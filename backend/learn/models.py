"""DB entities definitions.
"""
from random import randrange
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.functional import cached_property
from jsonfield import JSONField


class Chunk(models.Model):
    """Any entity in the programming domain.

    Currently: there are two types of chunks: problemsets and tasks.
    In the future, we might add: toolboxes, blocks, instructions, hints, concepts.
    """
    # The name of a chunk. Same name can be used for chunks of different type,
    # but not for the chunks of the same type.
    # be must be unique across all chunks.
    name = models.SlugField(blank=True, unique=False, default='')
    # All chunks have order to allow for ordered relationship.
    order = models.SmallIntegerField(default=0)

    # TODO: Consider to make type a field to allow enforcing unique_together
    # (type, name) on DB level.
    @property
    def type(self):
        """String specifying type of the entity (e.g. 'ps', 'task', 'tbx').
        """
        return ''  # To be overriden by subclasses.

    @property
    def qualified_name(self):
        return '{prefix}:{name}'.format(prefix=self.type, name=self.name)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{name}'.format(name=self.name)


class Block(models.Model):
    """Programming block, such as "fly" or "repeat".
    """
    name = models.CharField(max_length=256, unique=True)
    order = models.SmallIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Toolbox(models.Model):
    """Set of programming blocks
    """
    name = models.CharField(max_length=256, unique=True)
    blocks = models.ManyToManyField(Block)

    def __str__(self):
        return self.name


class Instruction(models.Model):
    """Explanation of a single concept, such as while loop or wormholes.
    """
    name = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class ProblemSet(Chunk):
    """Set of tasks practicing common concepts.
    """
    section = models.CharField(
        max_length=20, blank=True, default='',
        help_text="Dot-numbering '<mission>.<phase>', e.g. '3.4'.")
    # TODO: Extract from section (as a property / on save).
    level = models.SmallIntegerField(
        default=0,
        help_text='The top-most section number.')
    setting = JSONField(default=dict)
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True,
        related_name='parts')
    # tasks = 1:n relation with tasks

    MISSION = 'mission'
    PHASE = 'phase'
    GRANULARITY_CHOICES = ((MISSION, MISSION), (PHASE, PHASE))
    granularity = models.CharField(
        help_text='Hierachy level; either base phase, or compound mission.',
        max_length=10,
        choices=GRANULARITY_CHOICES,
        default=PHASE)

    # Reversed relationship from Chunks would be called 'problemset' by
    # default, which would clash with Task.problemset, so we rename it.
    chunk = models.OneToOneField(
        Chunk, on_delete=models.CASCADE, parent_link=True,
        related_name='problemset_obj')

    @property
    def type(self):
        return 'ps'

    @property
    def phases(self):
        assert self.granularity == self.MISSION
        return list(self.parts.all())

    # TODO: Consider to remove (use self.parent instead).
    @property
    def parent_mission(self):
        assert self.granularity == self.PHASE
        return self.parent

    # TODO: Caching.
    @property
    def n_tasks(self):
        return self.tasks.count()

    def __str__(self):
        return '{section} {name}'.format(section=self.section, name=self.name)


# TODO: Inhertit Task from Chunk
# (requires careful migrations, because some tasks already exist).
#class Task(Chunk):
class Task(models.Model):
    """Problem to be solved to practice programming.
    """
    problemset = models.ForeignKey(ProblemSet,
        on_delete=models.SET_NULL, null=True,
        related_name='tasks')
    setting = JSONField(default=dict)
    solution = models.TextField(blank=True, default='')
    # sessions = m:n relation with students through learn.TaskSession

    # TODO: Remove name and order once the inheritance migration is completed.
    name = models.SlugField(blank=True, unique=False, default='')
    order = models.SmallIntegerField(default=0)
    #chunk = models.OneToOneField(
    #    Chunk, on_delete=models.CASCADE, parent_link=True,
    #    related_name='task_obj')

    @property
    def type(self):
        return 'task'

    @property
    def mission(self):
        if self.problemset is None:
            return None
        return self.problemset.parent_mission

    @property
    def level(self):
        return self.problemset.level if self.problemset is not None else 0

    def get_absolute_url(self):
        return '/task/{name}/'.format(name=self.name)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    """Teacher can create classrooms and see progress of the students.
    """
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    # classrooms = 1:n relationship with Classroom entities

    @property
    def name(self):
        return self.user.get_full_name() if self.user else 'anonymous'

    def __str__(self):
        return '[{pk}] {name}'.format(pk=self.pk, name=self.name)


class Classroom(models.Model):
    """A group of students with a single teacher.
    """
    name = models.CharField(max_length=256, unique=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=False, related_name='classrooms')
    # students = 1:n relationship with Student entities

    def __str__(self):
        return self.name


class Student(models.Model):
    """Entity for a learner.
    """
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    credits = models.IntegerField(default=0)
    seen_instructions = models.ManyToManyField(Instruction)
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='students')
    # task_sessions = m:n relation with tasks through learn.TaskSession
    # skills = m:n relation with chunks through learn.Skill

    def get_skill(self, chunk):
        for skill in self.skills.all():
            if skill.chunk == chunk:
                return skill.value
        return 0

    def __str__(self):
        return 's{pk}'.format(pk=self.pk)


@receiver(post_save, sender=User)
def create_student(sender, instance, created, **kwargs):
    """Student is automatically created for a new user.
    """
    if created:
        Student.objects.create(user=instance)


class TaskSession(models.Model):
    """Continous attempt of a student to solve a task.
    """
    student = models.ForeignKey(Student, related_name='task_sessions')
    task = models.ForeignKey(Task, related_name='sessions')
    solved = models.BooleanField(default=False)
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=timezone.now)

    UNSOLVED = 0
    POOR = 1
    GOOD = 2
    EXCELLENT = 3
    PERFORMANCE_CHOICES = (
        (UNSOLVED, 'unsolved'),
        (POOR, 'poor'),
        (GOOD, 'good'),
        (EXCELLENT, 'excellent'))

    performance = models.SmallIntegerField(
        choices=PERFORMANCE_CHOICES,
        default=UNSOLVED)

    # Student can attempt a single task multiple times, but only the first
    # successful attempt is shown in stats and is used for skill compuation.
    # If the student hasn't solved the task yet, then the main task session is
    # the most recent one for given s-t pair.
    main = models.BooleanField(default=False)

    @property
    def time_spent(self):
        delta = self.end - self.start
        seconds = int(delta.total_seconds())
        return seconds

    @property
    def date(self):
        return self.end.date()

    def __str__(self):
        return '[{pk}] s{student}-{task}'.format(
            pk=self.pk,
            student=self.student.pk,
            task=self.task.name)


class Skill(models.Model):
    """Measure of mastery for each student-chunk pair
    """
    student = models.ForeignKey(Student, related_name='skills')
    chunk = models.ForeignKey(Chunk)
    value = models.FloatField(default=0)

    class Meta:
        unique_together = ('student', 'chunk')

    def __str__(self):
        return '{student}:{chunk}={value}'.format(
            student=self.student,
            chunk=self.chunk,
            value=self.value)


class ProgramSnapshot(models.Model):
    """Snapshot of a program at a point of time.
    """
    EXECUTION = 'execution'
    EDIT = 'edit'
    GRANULARITY_CHOICES = (
        (EXECUTION, EXECUTION),
        (EDIT, EDIT))

    task_session = models.ForeignKey(TaskSession, related_name='snapshots')
    time = models.DateTimeField(default=timezone.now)
    program = models.TextField()
    granularity = models.CharField(
        help_text='Level of snapshoptting frequency.',
        max_length=10,
        choices=GRANULARITY_CHOICES,
        default=EDIT)
    correct = models.NullBooleanField(
        help_text='Whether the snapshot is correct solution. Only applies for executions.',
        default=None)

    @property
    def program_shortened(self):
        if len(self.program) > 60:
            return self.program[:60] + '...'
        return self.program

    @cached_property
    def order(self):
        """Order of the snapshot for the granularity level and current task session.
        """
        # The filtering is done in plain Python to avoid excess SQL queries if
        # the snapshots are already prefetched.
        # TODO: Compute the order on save(). It's not going to change later, so
        # there no consistency issues.
        snapshots = self.task_session.snapshots.all()
        n_previous_snapshots = sum(
            1 for s in snapshots
            if s.granularity == self.granularity and s.time < self.time)
        order = n_previous_snapshots + 1
        return order

    @cached_property
    def time_from_start(self):
        """Number of seconds from the point when the student started the task session.
        """
        delta = self.time - self.task_session.start
        seconds = int(delta.total_seconds())
        return seconds

    def __str__(self):
        return '[{pk}] {program}'.format(pk=self.pk, program=self.program_shortened)


def generate_uuid_string():
    return uuid4().hex


class Domain(models.Model):
    """Describes the education content, concepts and relationships between them.

    This model allows to have a single object with prefetched domain entities,
    to easily deactivate some entities without deleting them (simply by
    removing them from the "current" domain), and using differnt domain for
    different users (AB experiments, testing version).
    """
    name = models.SlugField(unique=True, default=generate_uuid_string)
    # TODO: only set chunks, and access all chunk-types via @property
    #chunks = models.ManyToManyField(Chunk)
    blocks = models.ManyToManyField(Block)
    toolboxes = models.ManyToManyField(Toolbox)
    tasks = models.ManyToManyField(Task)
    problemsets = models.ManyToManyField(ProblemSet)

    def __str__(self):
        return str(self.name)


class DomainParam(models.Model):
    """Parameters linked to a domain, optionally to a specific chunk.
    """
    domain = models.ForeignKey(Domain, related_name='params')
    name = models.SlugField(unique=False)
    chunk = models.ForeignKey(Chunk, blank=True, null=True)
    value = models.FloatField(default=0)

    def __str__(self):
        identifiers = [
            str(entity)
            for entity in [self.domain, self.name, self.chunk]
            if entity is not None]
        return '{identifier}={value}'.format(
            identifier=':'.join(identifiers),
            value=self.value)


def generate_random_integer():
    return randrange(2**30)


class Action(models.Model):
    """All actions and events in the domain we model.
    """
    START_TASK = 'start-task'
    EDIT_PROGRAM = 'edit-program'
    RUN_PROGRAM = 'run-program'
    WATCH_INSTRUCTION = 'watch-instruction'
    ACTION_CHOICES = (
        (START_TASK, START_TASK),
        (EDIT_PROGRAM, EDIT_PROGRAM),
        (RUN_PROGRAM, RUN_PROGRAM),
        (WATCH_INSTRUCTION, WATCH_INSTRUCTION))

    name = models.CharField(
        help_text='One of the predefined types of actions.',
        max_length=20,
        choices=ACTION_CHOICES)
    student = models.ForeignKey(Student, null=True)
    task = models.ForeignKey(Task, null=True)
    time = models.DateTimeField(auto_now_add=True)
    randomness = models.IntegerField(default=generate_random_integer)
    data = JSONField(
        help_text='Unstructured part of the data (depends on the action type).')

    @property
    def instruction(self):
        return self.data['instruction']

    @property
    def snapshot(self):
        return self.data['snapshot']

    @property
    def correct(self):
        return self.data['correct']

    @property
    def task_session_id(self):
        return self.data['task_session_id']

    def __str__(self):
        return '[{pk}] {name}:s{student}:{task_or_instruction}'.format(
            pk=self.pk,
            name=self.name,
            student=self.student_id,
            task_or_instruction=(
                self.instruction if self.name == self.WATCH_INSTRUCTION
                else self.task.name))

    class Meta:
        ordering = ('time',)
