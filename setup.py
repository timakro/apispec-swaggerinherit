from setuptools import setup

setup(name='apispec-swaggerinherit',
      version='1.0.1',
      license='LGPLv3',
      description='Plugin for apispec adding support for Swagger-style '
                  'inheritance using `allOf`',
      author='Tim Schumacher',
      author_email='tim@timakro.de',
      url='https://github.com/timakro/apispec-swaggerinherit',
      install_requires=['apispec', 'marshmallow'],
      py_modules=['apispec_swaggerinherit']
      )
