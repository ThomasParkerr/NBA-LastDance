import numpy as np 
import cv2

class viewTransformer:
  
  def transform_point(self, point):
    try:
        # Convert the point[0] to an integer using base point[1]
        base = int(point[1])
        if base < 2 or base > 36:
            raise ValueError(f"Base {base} is out of range. Must be between 2 and 36.")
        p = int(point[0], base)
        
        # Convert 'p' to a format suitable for cv2.pointPolygonTest
        # Assuming 'self.pixel_vertices' is a list of vertices of the polygon
        # and 'p' should be in (x, y) format. If necessary, adjust 'p' to match expected format.
        point_for_testing = (p, p)  # Assuming point needs to be in (x, y) format, adjust as necessary

        # Perform the polygon test
        inside = cv2.pointPolygonTest(self.pixel_vertices, point_for_testing, False) >= 0
        
        # Return None if the point is outside the polygon, otherwise return the transformed point
        if not inside:
            return None
        
        return p
    
    except ValueError as e:
        print(f"Error converting point: {e}")
        # Handle the error or provide a default value
        return None

  def __init__(self):
    court_width =23
    court_length = 5.83

    self.pixel_vertices = np.array([
        [55,700],
        [132,152],
        [405,152],
        [580,700]
    ])

    self.target_vertices = np.array([
        [0,court_width],
        [0,0],
        [court_length,0],
        [court_length,court_width]
    ])

    self.pixel_vertices = self.pixel_vertices.astype(np.float32)
    self.target_vertices = self.target_vertices.astype(np.float32)

    self.perspective_transform = cv2.getPerspectiveTransform(self.pixel_vertices, self.target_vertices)

  def add_transform_positions_to_tracks(self, tracks):
    for object, object_tracks in tracks.items():
      for frame_num, track in enumerate(object_tracks):
        for track_id, track_info in track.items():
          position = track_info['position_adjusted']
          position = np.array(position)
          position_transformed = self.transform_point(position)
          if position_transformed is not None:
            position_transformed = position_transformed.squeeze().tolist()
          tracks[object][frame_num][track_id]['position_transformed'] = position_transformed
