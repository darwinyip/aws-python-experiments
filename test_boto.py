import boto3
from botocore.stub import Stubber
import unittest

class Foo:
	def __init__(self):
		self.dynamo_resource = boto3.resource('dynamodb', 'us-east-2')

	def bar(self):
		with self.dynamo_resource.Table('abc').batch_writer() as batch:
			for i in range(10):
				batch.put_item(Item={f"a_{i}": f"b_{i}"})

class TestBoto3(unittest.TestCase):
	def test_dynamo_db(self):
		dynamo_client = boto3.client('dynamodb', 'us-east-2')
		dynamo_stub = Stubber(dynamo_client)
		foo = Foo()
		foo.dynamo_resource.meta.client = dynamo_client
		dynamo_stub.add_response('batch_write_item', {'UnprocessedItems': {}})
		with dynamo_stub:
			foo.bar()

if __name__ == '__main__':
    unittest.main()