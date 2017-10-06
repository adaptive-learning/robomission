from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from learn.models import Block
from learn.serializers import BlockSerializer


@api_view(['GET', 'POST'])
def block_list(request, format=None):
    """List all blocks, or create a new block.
    """
    if request.method == 'GET':
        blocks = Block.objects.all()
        serializer = BlockSerializer(blocks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BlockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
def block_detail(request, pk, format=None):
    """Retrieve, update or delete a block instance.
    """
    try:
        block = Block.objects.get(pk=pk)
    except Block.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BlockSerializer(block)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BlockSerializer(block, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        block.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
