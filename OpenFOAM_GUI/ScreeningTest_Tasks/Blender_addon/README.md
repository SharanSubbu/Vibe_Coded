# Custom Cube Addon for Blender

This Blender addon provides a specialized toolkit for generating, managing, and merging cube-based mesh structures. The UI helps to evenly distribute N cubes into a 2D array.

## Installation

1. Download and save a copy of the provided Python script `custom_cube_addon.py`.
2. Launch Blender 5.0.
3. Go to `Edit > Preferences > Add-ons`.
4. Click the **Install from Disk...** button at the top right of the window to open a file browser window.
5. Navigate to the path of `custom_cube_addon.py`, select it and click **Install Add-on**.
6. Locate **Mesh: Custom Cube Addon** in the list and check the box to activate it.

## Usage

### 1. Generating Cubes
- Locate the **Cube Tools** tab in the Sidebar of the 3D Viewport (Press `N` to toggle).
- Input a natural number below 20 in the **Number of Cubes** field.
- Click **Distribute** to generate the array.

### 2. Selection
- **Single Select**: Left-click a cube.
- **Multi-Select**: Hold **Shift** and left-click cubes.
- **Box Select**: To select multiple cubes quickly, hold **Shift and drag your mouse** to draw a selection border over the desired objects.

### 3. Deleting Cubes
- Select the cubes you wish to remove.
- Click **Delete Selected Cubes**. 
- *Note: If a Camera or Light is in the selection, the operation will be cancelled with a warning to protect scene infrastructure.*

### 4. Merging (Compose Mesh)
- Select at least two cubes that share a common face (touching side-by-side).
- Click **Merge Shared Faces**.
- **The Algorithm**: 
    1. The script joins the objects into a single data block.
    2. Overlapping vertices are merged within a 0.001 threshold.
    3. `limited_dissolve` is applied to eliminate interior faces, resulting in a clean, manifold outer shell.
    