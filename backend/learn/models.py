"""DB entities definitions.
"""
import json
from random import randrange
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User
from django.db.models import prefetch_related_objects, Prefetch
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
    # Type of the chunk, e.g 'tbx', or 'task'.  Can be overriden by subclass.
    # Can contain field placeholders, e.g. 'ps.{field:granularity}'.
    TYPE = ''
    type = models.CharField(max_length=256, blank=True, default='')

    # The name of a chunk. Same name can be used for chunks of different type,
    # but not for the chunks of the same type.
    # be must be unique across all chunks.
    name = models.SlugField(blank=True, unique=False, default='')

    # All chunks have order to allow for ordered relationship.
    # Integer list is depcreacted, and string representation does not allow
    # for correct ordering at DB level (becasue '10' < '9'), so we manually
    # define fields for all possible sublevel.
    level = models.PositiveSmallIntegerField(blank=True, null=True, default=None)
    level2 = models.PositiveSmallIntegerField(blank=True, null=True, default=None)
    level3 = models.PositiveSmallIntegerField(blank=True, null=True, default=None)

    content = JSONField(
        default=dict,
        help_text='Description, setting, solution, etc.')

    class Meta:
        ordering = ['type', 'level', 'level2', 'level3']

    def __init__(self, *args, **kwargs):
        # Inject type (unless already set).
        if 'type' not in kwargs:
            kwargs['type'] = self._interpolate_type(**kwargs)
        super(Chunk, self).__init__(*args, **kwargs)

    def _interpolate_type(self, **kwargs):
        """Return type based on self.TYPE, and provided kwargs or defaults.
        """
        parts = self.TYPE.split('.')
        for i, part in enumerate(parts):
            if part.startswith('{field:'):
                field_name = part[7:-1]  # cut 'name' from '{field:name}'
                # Explicit test for inclusion in kwargs to avoid computing
                # default value if it is not necessary.
                if field_name in kwargs:
                    parts[i] = kwargs[field_name]
                else:
                    parts[i] = self._meta.get_field(field_name).get_default()
        return '.'.join(parts)

    @property
    def levels(self):
        """List of numberical levels, e.g. [2, 3, 7].

        Missing levels preceding a non-zero level are filled as 0,
        e.g. None,2,None --> [0, 2].
        """
        nums = [(lvl or 0) for lvl in [self.level, self.level2, self.level3]]
        for i, lvl in reversed(list(enumerate(nums))):
            if lvl != 0:
                return nums[:i+1]
        return [0]

    @levels.setter
    def levels(self, value):
        self.level = value[0]
        if len(value) >= 2:
            self.level2 = value[1]
        if len(value) >= 3:
            self.level3 = value[2]

    @property
    def section(self):
        """Dotted representation of the full order, e.g. '3.4'.
        """
        return '.'.join(map(str, self.levels))

    @section.setter
    def section(self, value):
        self.levels = [int(lvl) for lvl in value.split('.')]

    @property
    def order(self):
        """The last part of the section number.
        """
        return self.levels[-1]

    @order.setter
    def order(self, value):
        # TODO: Make it more robust (e.g when both level and order is set in
        # init)
        self.levels = self.levels[:-1] + [value]

    @property
    def qualified_name(self):
        if self.type:
            return '{prefix}:{name}'.format(prefix=self.type, name=self.name)
        return self.name

    #@property
    #def description(self):
    #    """Only some chunks have description.
    #    """
    #    return self.content.get('description', '')

    @property
    def setting(self):
        """Only some chunks have setting (problem sets and tasks).
        """
        return self.content.get('setting', {})

    @setting.setter
    def setting(self, value):
        self.content['setting'] = value

    @property
    def solution(self):
        """Only some chunks have solution (tasks).
        """
        return self.content.get('solution', '')

    @solution.setter
    def solution(self, value):
        self.content['solution'] = value

    # Hack to overcome a bug in JsonField implementation that results in
    # not parsing json values in inherited models, leaving them as strings
    # See https://github.com/dmkoch/django-jsonfield/issues/101.
    # TODO: Use another JsonField implementation, or subclass the current one
    # and override the problematic part (see the referenced issue).
    @classmethod
    def from_db(cls, db, field_names, values):
        for i, (name, value) in enumerate(zip(field_names, values)):
            if name == 'content' and isinstance(value, str):
                value_list = list(values)
                value_list[i] = json.loads(value)
                values = tuple(value_list)
                break
        return super(Chunk, cls).from_db(db, field_names, values)

    def __str__(self):
        return self.qualified_name
        #return '{section} {name}'.format(
        #    section=self.section, name=self.qualified_name)


# TODO: Move to a custom Chunk manager.
# TODO: Add unit tests.
def get_chunk(qualified_name):
    chunk_type, name = qualified_name.split(':')
    for model in [Task, ProblemSet]:
        model_type = model.TYPE.split('.')[0]
        if chunk_type == model_type:
            return model.objects.get(name=name)
    raise Chunk.DoesNotExist('No chunk "{0}".'.format(qualified_name))


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


class Instruction(Chunk):
    """Explanation of a single concept, such as while loop or wormholes.
    """
    TYPE = 'instruction'
    chunk_ptr = models.OneToOneField(
        Chunk, on_delete=models.CASCADE, parent_link=True,
        related_name='instruction_obj')

    def __str__(self):
        return self.name


class ProblemSetManager(models.Manager):
    pass


class MissionManager(ProblemSetManager):
    def get_queryset(self):
        return super().get_queryset().filter(granularity=self.model.MISSION)

    def squeeze_sections(self):
        """Update sections of all missions to remove gaps.
        """
        # TODO?: Optimize to single SQL query / less of them.
        for i, mission in enumerate(self.get_queryset(), start=1):
            mission.section = str(i)
            mission.save()  # save() propagates the changes


class ProblemSet(Chunk):
    """Set of tasks practicing common concepts.
    """
    TYPE = 'ps.{field:granularity}'
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
        default=MISSION)

    # Reversed relationship from Chunks would be called 'problemset' by
    # default, which would clash with Task.problemset, so we rename it.
    # TODO: rename to chunk_obj (/chunk_ptr/chunk_ref) to avoid mission.chunk
    # which had different meaning before.
    chunk = models.OneToOneField(
        Chunk, on_delete=models.CASCADE, parent_link=True,
        related_name='problemset_obj')

    objects = ProblemSetManager()
    missions = MissionManager()

    class Meta:
        base_manager_name = 'objects'

    def __init__(self, *args, **kwargs):
        # Infer granularity from parent.
        parent = kwargs.get('parent', None)
        granularity = ProblemSet.PHASE if parent else ProblemSet.MISSION
        if 'granularity' in kwargs:
            assert kwargs['granularity'] == granularity
        kwargs['granularity'] = granularity
        super().__init__(*args, **kwargs)
        self.__initial_section = self.section

    @property
    def is_mission(self):
        return self.granularity == self.MISSION

    @property
    def phases(self):
        assert self.is_mission
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

    @property
    def n_parts(self):
        return self.parts.count()

    def add_part(self, *args, **kwargs):
        kwargs['parent'] = self
        kwargs['granularity'] = 'phase'
        kwargs['section'] = '{0}.{1}'.format(self.section, self.n_parts+1)
        ps = ProblemSet.objects.create(*args, **kwargs)
        return ps

    def set_parts(self, parts, squeeze_sections=False):
        """Set parts; infer and propagate sections and granularity.
        """
        self.parts.set(parts)  # also removes old relationships
        for i, part in enumerate(parts, start=1):
            part.parent = self
            part.granularity = ProblemSet.PHASE
            part.levels = self.levels + [i]
            part.save()
        if squeeze_sections:
            ProblemSet.missions.squeeze_sections()
            self.refresh_from_db()
            for part in parts:
                part.refresh_from_db()

    def add_task(self, *args, **kwargs):
        kwargs['problemset'] = self
        kwargs['section'] = '{0}.{1}'.format(self.section, self.n_tasks+1)
        task = Task.objects.create(*args, **kwargs)
        return task

    def set_tasks(self, tasks):
        """Set tasks including their section numbers.
        """
        self.tasks.set(tasks)  # also removes old relationships
        for i, task in enumerate(tasks, start=1):
            task.problemset = self
            task.section = '{0}.{1}'.format(self.section, i)
            task.save()

    def save(self, *args, **kwargs):
        # Infer granularity from parent.
        self.granularity = ProblemSet.PHASE if self.parent else ProblemSet.MISSION
        # TODO: Make the syncronization between granularity and type more
        # explicit (to avoid desynchronization by mistake).
        self.type = self._interpolate_type(granularity=self.granularity)
        # TODO(once Chunk.parent exists):
        # Move section setting to section.default function.
        # TODO: Make it more robust (e.g. if some sections have out-of-ordering
        # section, or when there are multiple domains).
        if not self.section or self.section == '0':
            if self.parent:
                subsection = self.parent.n_parts + 1
                self.section = '{0}.{1}'.format(self.parent.section, subsection)
            else:
                top_sections = ProblemSet.objects.filter(parent__isnull=True)
                self.section = str(top_sections.count() + 1)
        super(ProblemSet, self).save(*args, **kwargs)
        # Propagate section changes
        if self.section != self.__initial_section and self.section:
            for i, part in enumerate(self.parts.all(), start=1):
                part.section = '{0}.{1}'.format(self.section, i)
                part.save()
            for i, task in enumerate(self.tasks.all(), start=1):
                task.section = '{0}.{1}'.format(self.section, i)
                task.save()


    def __str__(self):
        # Overrides the parent __str__ to omit prefix (type).
        return self.name


class Task(Chunk):
    """Problem to be solved to practice programming.
    """
    TYPE = 'task'
    problemset = models.ForeignKey(ProblemSet,
        on_delete=models.SET_NULL, null=True,
        related_name='tasks')
    # sessions = m:n relation with students through learn.TaskSession

    chunk_ptr = models.OneToOneField(
        Chunk, on_delete=models.CASCADE, parent_link=True,
        related_name='task_obj')

    @property
    def mission(self):
        if self.problemset is None:
            return None
        return self.problemset.parent_mission

    def get_absolute_url(self):
        return '/task/{name}/'.format(name=self.name)

    def __str__(self):
        # Overrides the parent __str__ to omit prefix (type).
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

    def get_skill(self, chunk, cached=False):
        """Retrieve the current or cached skill.
        """
        if cached:
            self.cache_skills(update=False)
            # It's important to test PK due to inheritance (Chunk vs. ProblemSet)
            skills = [s for s in self.cached_skills if chunk.pk == s.chunk.pk]
            skill = skills[0] if skills else None
        else:
            skill = self.skills.filter(chunk=chunk).first()
        return skill.value if skill else 0

    def cache_skills(self, update=True):
        if not update and hasattr(self, 'cached_skills'):
            return
        prefetch_related_objects([self], Prefetch('skills', to_attr='cached_skills'))

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
    instructions = models.ManyToManyField(Instruction)

    @cached_property
    def missions(self):
        return (
            self.problemsets
            .filter(granularity=ProblemSet.MISSION)
            # We prefetch parts of parts (even though they are currently empty)
            # to avoid unwanted SQL queries, e.g. in mastery.has_mastered.
            .prefetch_related('tasks', 'parts', 'parts__parts'))

    def __str__(self):
        return str(self.name)


class DomainParam(models.Model):
    """Parameters linked to a domain, optionally to a specific chunk.
    """
    domain = models.ForeignKey(Domain, related_name='params')
    name = models.SlugField(unique=False)
    chunk = models.ForeignKey(Chunk, blank=True, null=True)
    value = models.FloatField(default=0)

    class Meta:
        unique_together = ('domain', 'name', 'chunk')

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
