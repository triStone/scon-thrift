scon-thrift
===========

python file for generating thrift file for scons

Example
```
import os

env = Environment(
  ENV = {'PATH' : os.environ['PATH']},
  CCFLAGS=['-g', '-DHAVE_INTTYPES_H', '-DHAVE_NETINET_IN_H', '-Wall', '-std=c++11'],
  tools=['default', 'thrift'],
  toolpath = ['./']
)

thrift_files = env.Thrift(
  [],
  'interface.thrift'
)

target = env.Library('interface', thrift_files)
```
