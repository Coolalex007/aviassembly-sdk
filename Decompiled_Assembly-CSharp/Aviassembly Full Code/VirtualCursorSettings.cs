using System;
using System.IO;
using UnityEngine;
using UnityEngine.InputSystem;

[Serializable]
public class VirtualCursorSettings
{
	public string moveCursorOverride;

	public string zoomOverride;

	public string leftButtonOverride;

	public string rightButtonOverride;

	public string slowCursorOverride;

	public float cursorSpeed;

	public float slowdownSpeed;

	public void GetCurrentSettings(MouseInput input)
	{
		moveCursorOverride = input.moveCursorAction.SaveBindingOverridesAsJson();
		zoomOverride = input.zoomAction.SaveBindingOverridesAsJson();
		leftButtonOverride = input.leftButtonAction.SaveBindingOverridesAsJson();
		rightButtonOverride = input.rightButtonAction.SaveBindingOverridesAsJson();
		slowCursorOverride = input.slowCursorAction.SaveBindingOverridesAsJson();
		cursorSpeed = input.cursorSpeed;
		slowdownSpeed = input.mouseSlowdown;
	}

	public void ApplySettings(MouseInput input)
	{
		input.moveCursorAction.LoadBindingOverridesFromJson(moveCursorOverride);
		input.zoomAction.LoadBindingOverridesFromJson(zoomOverride);
		input.leftButtonAction.LoadBindingOverridesFromJson(leftButtonOverride);
		input.rightButtonAction.LoadBindingOverridesFromJson(rightButtonOverride);
		input.slowCursorAction.LoadBindingOverridesFromJson(slowCursorOverride);
		input.cursorSpeed = cursorSpeed;
		input.mouseSlowdown = slowdownSpeed;
	}

	public void SaveKeybinds()
	{
		if (!File.Exists(Application.persistentDataPath + "/virtualCursorSettings.json"))
		{
			using (File.CreateText(Application.persistentDataPath + "/virtualCursorSettings.json"))
			{
			}
		}
		string contents = JsonUtility.ToJson(this);
		File.WriteAllText(Application.persistentDataPath + "/virtualCursorSettings.json", contents);
	}

	public void LoadKeybinds()
	{
		if (File.Exists(Application.persistentDataPath + "/virtualCursorSettings.json"))
		{
			VirtualCursorSettings virtualCursorSettings = JsonUtility.FromJson<VirtualCursorSettings>(File.ReadAllText(Application.persistentDataPath + "/virtualCursorSettings.json"));
			moveCursorOverride = virtualCursorSettings.moveCursorOverride;
			zoomOverride = virtualCursorSettings.zoomOverride;
			leftButtonOverride = virtualCursorSettings.leftButtonOverride;
			rightButtonOverride = virtualCursorSettings.rightButtonOverride;
			slowCursorOverride = virtualCursorSettings.slowCursorOverride;
			cursorSpeed = virtualCursorSettings.cursorSpeed;
			slowdownSpeed = virtualCursorSettings.slowdownSpeed;
		}
	}
}
