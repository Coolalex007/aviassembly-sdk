using System.Collections.Generic;
using System.IO;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.Controls;

public class InputManager : Singleton<InputManager>
{
	public float throttleInput;

	public float rollInput;

	public float yawInput;

	public float pitchInput;

	public bool wheelRetraction;

	public InputBlocker currentInputBlocker;

	private Dictionary<Keys, string> displayStrings = new Dictionary<Keys, string>();

	private Dictionary<Keys, string> primaryBindingPath = new Dictionary<Keys, string>();

	private Dictionary<Keys, string> secondaryBindingPath = new Dictionary<Keys, string>();

	public PlayerInput playerInput;

	public ControlScheme CurrentControlSceme { get; private set; }

	protected override void Awake()
	{
		base.Awake();
		RefreshDisplayNames();
		RefreshBindingPaths();
		playerInput.onControlsChanged += OnControlsChanged;
	}

	private void OnControlsChanged(PlayerInput input)
	{
		if (input.currentControlScheme == "keyboard")
		{
			CurrentControlSceme = ControlScheme.KeyboardAndMouse;
		}
		if (input.currentControlScheme == "gamepad")
		{
			CurrentControlSceme = ControlScheme.Gamepad;
		}
	}

	public void RefreshDisplayNames()
	{
		displayStrings.Clear();
		displayStrings.Add(Keys.PitchUp, playerInput.actions["Pitch"].bindings[1].ToDisplayString());
		displayStrings.Add(Keys.PitchDown, playerInput.actions["Pitch"].bindings[2].ToDisplayString());
		displayStrings.Add(Keys.RollLeft, playerInput.actions["Roll"].bindings[1].ToDisplayString());
		displayStrings.Add(Keys.RollRight, playerInput.actions["Roll"].bindings[2].ToDisplayString());
		displayStrings.Add(Keys.YawLeft, playerInput.actions["Yaw"].bindings[1].ToDisplayString());
		displayStrings.Add(Keys.YawRight, playerInput.actions["Yaw"].bindings[2].ToDisplayString());
		displayStrings.Add(Keys.Break, playerInput.actions["Throttle"].bindings[1].ToDisplayString());
		displayStrings.Add(Keys.Forward, playerInput.actions["Throttle"].bindings[2].ToDisplayString());
		displayStrings.Add(Keys.RetractGear, playerInput.actions["WheelRetraction"].bindings[0].ToDisplayString());
	}

	public void RefreshBindingPaths()
	{
		primaryBindingPath.Clear();
		secondaryBindingPath.Clear();
		primaryBindingPath.Add(Keys.PitchUp, playerInput.actions["Pitch"].bindings[1].effectivePath);
		primaryBindingPath.Add(Keys.PitchDown, playerInput.actions["Pitch"].bindings[2].effectivePath);
		primaryBindingPath.Add(Keys.RollLeft, playerInput.actions["Roll"].bindings[1].effectivePath);
		primaryBindingPath.Add(Keys.RollRight, playerInput.actions["Roll"].bindings[2].effectivePath);
		primaryBindingPath.Add(Keys.YawLeft, playerInput.actions["Yaw"].bindings[1].effectivePath);
		primaryBindingPath.Add(Keys.YawRight, playerInput.actions["Yaw"].bindings[2].effectivePath);
		primaryBindingPath.Add(Keys.Break, playerInput.actions["Throttle"].bindings[1].effectivePath);
		primaryBindingPath.Add(Keys.Forward, playerInput.actions["Throttle"].bindings[2].effectivePath);
		primaryBindingPath.Add(Keys.RetractGear, playerInput.actions["WheelRetraction"].bindings[0].effectivePath);
		secondaryBindingPath.Add(Keys.PitchUp, playerInput.actions["Pitch"].bindings[4].effectivePath);
		secondaryBindingPath.Add(Keys.PitchDown, playerInput.actions["Pitch"].bindings[5].effectivePath);
		secondaryBindingPath.Add(Keys.RollLeft, playerInput.actions["Roll"].bindings[4].effectivePath);
		secondaryBindingPath.Add(Keys.RollRight, playerInput.actions["Roll"].bindings[5].effectivePath);
		secondaryBindingPath.Add(Keys.YawLeft, playerInput.actions["Yaw"].bindings[4].effectivePath);
		secondaryBindingPath.Add(Keys.YawRight, playerInput.actions["Yaw"].bindings[5].effectivePath);
		secondaryBindingPath.Add(Keys.Break, playerInput.actions["Throttle"].bindings[4].effectivePath);
		secondaryBindingPath.Add(Keys.Forward, playerInput.actions["Throttle"].bindings[5].effectivePath);
		secondaryBindingPath.Add(Keys.RetractGear, playerInput.actions["WheelRetraction"].bindings[1].effectivePath);
	}

	public string GetKeyPath(Keys key, ControlScheme controlScheme)
	{
		if (controlScheme == ControlScheme.KeyboardAndMouse && primaryBindingPath.ContainsKey(key))
		{
			return primaryBindingPath[key];
		}
		if (controlScheme == ControlScheme.Gamepad && secondaryBindingPath.ContainsKey(key))
		{
			return secondaryBindingPath[key];
		}
		return "";
	}

	public InputActionRebindingExtensions.RebindingOperation StartKeyRebind(Keys key, ControlScheme controlScheme)
	{
		int num = ((controlScheme == ControlScheme.Gamepad) ? 3 : 0);
		if (key == Keys.RetractGear && num == 3)
		{
			num = 1;
		}
		return key switch
		{
			Keys.PitchUp => RebindAction("Pitch", 1 + num), 
			Keys.PitchDown => RebindAction("Pitch", 2 + num), 
			Keys.RollLeft => RebindAction("Roll", 1 + num), 
			Keys.RollRight => RebindAction("Roll", 2 + num), 
			Keys.YawLeft => RebindAction("Yaw", 1 + num), 
			Keys.YawRight => RebindAction("Yaw", 2 + num), 
			Keys.Break => RebindAction("Throttle", 1 + num), 
			Keys.Forward => RebindAction("Throttle", 2 + num), 
			Keys.RetractGear => RebindAction("WheelRetraction", num), 
			_ => null, 
		};
	}

	private void Start()
	{
		LoadKeybinds();
		RefreshDisplayNames();
		RefreshBindingPaths();
	}

	private void Update()
	{
		pitchInput = playerInput.actions["Pitch"].ReadValue<float>();
		rollInput = playerInput.actions["Roll"].ReadValue<float>();
		yawInput = playerInput.actions["Yaw"].ReadValue<float>();
		throttleInput = playerInput.actions["Throttle"].ReadValue<float>();
		wheelRetraction = playerInput.actions["WheelRetraction"].WasPressedThisFrame();
	}

	public InputActionRebindingExtensions.RebindingOperation RebindAction(string actionName, int index)
	{
		InputAction inputAction = playerInput.actions[actionName];
		inputAction.Disable();
		_ = inputAction.bindings[index].overridePath;
		return inputAction.PerformInteractiveRebinding(index).WithControlsExcluding("Mouse").WithCancelingThrough("<keyboard>/escape")
			.WithMagnitudeHavingToBeGreaterThan(0f)
			.WithExpectedControlType<ButtonControl>()
			.OnMatchWaitForAnother(0.1f)
			.OnCancel(delegate(InputActionRebindingExtensions.RebindingOperation operation)
			{
				operation.action.Enable();
				operation.Dispose();
			})
			.OnComplete(delegate(InputActionRebindingExtensions.RebindingOperation operation)
			{
				operation.action.Enable();
				operation.Dispose();
			})
			.Start();
	}

	public static InputActionRebindingExtensions.RebindingOperation RebindAction(InputAction action, int index)
	{
		action.Disable();
		_ = action.bindings[index].overridePath;
		return action.PerformInteractiveRebinding(index).WithControlsExcluding("Mouse").WithCancelingThrough("<keyboard>/escape")
			.WithMagnitudeHavingToBeGreaterThan(0f)
			.OnMatchWaitForAnother(0.1f)
			.OnCancel(delegate(InputActionRebindingExtensions.RebindingOperation operation)
			{
				operation.action.Enable();
				operation.Dispose();
			})
			.OnComplete(delegate(InputActionRebindingExtensions.RebindingOperation operation)
			{
				operation.action.Enable();
				operation.Dispose();
			})
			.Start();
	}

	public void SaveKeybinds()
	{
		if (!File.Exists(Application.persistentDataPath + "/keybinds.json"))
		{
			using (File.CreateText(Application.persistentDataPath + "/keybinds.json"))
			{
			}
		}
		string contents = playerInput.currentActionMap.SaveBindingOverridesAsJson();
		File.WriteAllText(Application.persistentDataPath + "/keybinds.json", contents);
	}

	private void LoadKeybinds()
	{
		if (File.Exists(Application.persistentDataPath + "/keybinds.json"))
		{
			string json = File.ReadAllText(Application.persistentDataPath + "/keybinds.json");
			playerInput.currentActionMap.LoadBindingOverridesFromJson(json);
		}
	}
}
