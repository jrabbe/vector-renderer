# Vector Renderer

A python based rendering engine for rendering 3D triangle meshes into images using vector
primitives. This renderer depends on the PlotDevice [1] package and can
render the provided triangle mesh to either an SVG, PNG, or GIF file.

The renderer is single-threaded and completely CPU bound (for now).

The files read in are tightly packged binary representations of the vertices, normals, and
optionally textures. **Note, textures are not supported for now.**

## Usage

After installing [PlotDevice] [1] (I recommend using a [virtual environment][2]), simply run the base script. The `-h` flag will show the available
options.

### Virtual Environmant

To install a virtual environment run the command

```bash
python3 -m venv env
```

The env folder is ignored in the `.gitignore`, so it's helpful calling the virtual environment by this name.

Then activate the virtual environment by running

```bash
source env/bin/activate
```

Also has support for csh and fish.

[1]: http://plotdevice.io/ "PlotDevice"
[2]: https://docs.python.org/3/tutorial/venv.html "Virtual Environment and Packages"
