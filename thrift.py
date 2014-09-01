import os
import SCons.Util
from SCons.Script import Builder, Action, Dir, File, Entry

thrift = 'thrift'

def GetServiceName(filename):
  for line in file(filename):
    l = line.strip().split()
    if len(l) > 1 and l[0] == 'service':
      return l[1]
  return None

def ThriftEmitter(target, source, env):
  dirOfCallingSconscript = Dir('.').srcnode()
  env.Prepend(THRIFTPATH = dirOfCallingSconscript.path)

  source_with_corrected_path = []
  for src in source:
    commonprefix = os.path.commonprefix([dirOfCallingSconscript.path, src.srcnode().path])
    if len(commonprefix) > 0:
      source_with_corrected_path.append(src.srcnode().path[len(commonprefix + os.sep):])
    else:
      source_with_corrected_path.append(src.srcnode().path)
  source = source_with_corrected_path

  for src in source:
    modulename = os.path.splitext(src)[0]
    if env['THRIFTCPPSOUT']:
      base = os.path.join(env['THRIFTCPPSOUT'], modulename)
      target.extend([base + '_constants.h', base + '_constants.cpp',
                  base + '_types.h', base + '_types.cpp'])
      service_name = GetServiceName(src)
      if service_name:
        base2 = os.path.join(env['THRIFTCPPSOUT'], service_name)
        target.extend([base2 + '.h', base2 + '.cpp', base2 + '_server.skeleton.cpp'])
  return target, source

ThriftAction = SCons.Action.Action('$THRIFTCOM', '$THRIFTCOMSTR')

ThriftBuilder = SCons.Builder.Builder(action = ThriftAction,
                                      emitter = ThriftEmitter,
                                      srcsuffix = '$THRIFTSRCSUFFIX')

def generate(env):
  try:
    bld = env['BUILDERS']['Thrift']
  except KeyError:
    bld = ThriftBuilder
    env['BUILDERS']['Thrift'] = bld

  env['THRIFT'] = env.Detect(thrift) or 'thrift'
  env['THRIFTFLAGS'] = SCons.Util.CLVar('')
  env['THRIFTCPPSOUT'] = 'gen-cpp/'
  env['THRIFTABSCPPSOUT'] = os.path.join(Dir('.').path, env['THRIFTCPPSOUT'])
  env['THRIFTCOM'] = '$THRIFT -out ${THRIFTABSCPPSOUT} --gen cpp ${SOURCES}'
  env['THRIFTSUFFIX'] = '.thrift'

def exists(env):
  return env.Detect(thrift)
