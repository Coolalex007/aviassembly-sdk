using UnityEngine;

public class CameraModeToggle : MonoBehaviour
{
	public CameraController cameraController;

	public void Click()
	{
		int cameraMode = (int)cameraController.cameraMode;
		cameraMode--;
		if (cameraMode < 0)
		{
			cameraMode = 2;
		}
		cameraController.SetCameraMode(cameraMode);
	}
}
