using TMPro;
using UnityEngine.InputSystem;
using UnityEngine.UI;

public class EngineSettings : PartSettingsBase
{
	public Toggle invertToggle;

	public Slider maxPower;

	public TMP_Text backwardRebindText;

	public TMP_Text forwardRebindText;

	private Engine engine;

	private InputActionRebindingExtensions.RebindingOperation forwaredRebinding;

	private InputActionRebindingExtensions.RebindingOperation backwardRebinding;

	private void Update()
	{
		engine.invertDirection = invertToggle.isOn;
		engine.maxPower = maxPower.value;
		forwardRebindText.text = engine.throttleInputOverride.bindings[2].ToDisplayString();
		backwardRebindText.text = engine.throttleInputOverride.bindings[1].ToDisplayString();
		if (forwaredRebinding != null)
		{
			forwardRebindText.text = "-";
			if (forwaredRebinding.completed || forwaredRebinding.canceled)
			{
				forwaredRebinding = null;
			}
		}
		if (backwardRebinding != null)
		{
			backwardRebindText.text = "-";
			if (backwardRebinding.completed || backwardRebinding.canceled)
			{
				backwardRebinding = null;
			}
		}
	}

	public void CancelRebind()
	{
		if (forwaredRebinding != null)
		{
			forwaredRebinding.Cancel();
			forwaredRebinding = null;
		}
		if (backwardRebinding != null)
		{
			backwardRebinding.Cancel();
			backwardRebinding = null;
		}
	}

	public void StartForwardOverride()
	{
		forwaredRebinding = InputManager.RebindAction(engine.throttleInputOverride, 2);
	}

	public void StartBackwardOverride()
	{
		backwardRebinding = InputManager.RebindAction(engine.throttleInputOverride, 1);
	}

	public override void SelectPart(PlanePart part)
	{
		engine = (Engine)part;
		invertToggle.SetIsOnWithoutNotify(engine.invertDirection);
		maxPower.SetValueWithoutNotify(engine.maxPower);
		forwardRebindText.text = engine.throttleInputOverride.bindings[2].ToDisplayString();
		backwardRebindText.text = engine.throttleInputOverride.bindings[1].ToDisplayString();
	}

	private void OnDisable()
	{
		CancelRebind();
	}
}
