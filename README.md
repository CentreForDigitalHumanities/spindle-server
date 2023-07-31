## Spindle Server

This repository contains a Dockerfile that can be used to create an image for a Spindle parser, wrapped in a very simple Flask webserver.

NB: the current image is broken and the container will immediately exit upon starting it. The following error is thrown:

```
terminate called after throwing an instance of 'std::bad_alloc'
what():  std::bad_alloc
```

**Setup**

1. Put a copy of `model_weights.pt` in the root directory. (This file is too large to check in on GitHub.)

2. Build an image with `docker build -t spindle-server:latest .`

3. Run container and expose ports. `docker run -d -P --name spindle-server spindle-server`
