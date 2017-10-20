from django.test import TestCase
from learn.models import Block


class BlockTestCase(TestCase):
    def test_blocks_exists(self):
        assert Block.objects.exists()

    def test_blocks_are_ordered(self):
        first_retrieved_blocks = list(Block.objects.all())[:3]
        first_expected_blocks = [
            Block.objects.get(name='fly'),
            Block.objects.get(name='shoot'),
            Block.objects.get(name='repeat')]
        assert first_retrieved_blocks == first_expected_blocks

    def test_str_returns_name(self):
        fly_block = Block.objects.get(name='fly')
        assert str(fly_block) == 'fly'
