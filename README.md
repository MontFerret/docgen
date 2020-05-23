Tool to generate documentation representations for standard ferret library from pseudo-static
analysis of go source code. This tool depends on a few regex patterns to find the available
methods and assumes a standard non-forgiving comment syntax for method implementations.

### Usage Information

1. The associated scripts require Python 3.6+
2. Make sure you install the required dependencies (check `requirements.txt`).
   You can use `pip3 install -r requirements.txt`
3. Change to the root project directory and run `tools/docs/stdlib/doc-gen pkg/stdlib/`. It should generate
   a YAML file which contains necessary information to generate documentation.

### Building Frontend

1. montferret.github.io has recipes to turn the YAML representations into themed docs.
