# Path generator
-	Build with Python and tkinter, path generator app is a tool to generate animation paths from .jpeg images
-	Allows users to pass parameters to image processing algorithm and filter processed images
-	Includes simulation feature to illustrate generated paths
-	Can be used to create a drawing game for example
- Follows principles of Model-View-Controller architecture

Program outputs .json file containing continius 3D curve:

 ```json
[
 {
  "x": 1,
  "y": 1,
  "z": 1
 },
 {
  "x": 2,
  "y": 2,
  "z": 2
 },
 {
  "x": 3,
  "y": 3,
  "z": 3
 },
 ...jne
```

### Web demonstration
- Rendering path on web page 
- [https://codesandbox.io/s/drawing-demo-zfzqjv?file=/src/Canvas.js](https://codesandbox.io/s/drawing-demo-zfzqjv?file=/src/Canvas.js)

## Libraries used

1. tkinter
2. opencv-python
3. Pillow
4. Scipy


## GIF
<img src="https://github.com/svhein/gif/blob/main/lentsikka2.gif" height="600" width="800" />