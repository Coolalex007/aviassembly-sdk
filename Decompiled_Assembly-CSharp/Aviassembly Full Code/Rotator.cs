using UnityEngine;
using UnityEngine.InputSystem;

public class Rotator : PlanePart
{
	public float speed;

	public InputAction inputOverride;

	public Transform rotatorBase;

	private BuildingPart part;

	private float rotation;

	private void Awake()
	{
		part = GetComponent<BuildingPart>();
		inputOverride = new InputAction("ThrottleInput");
		inputOverride.AddCompositeBinding("Axis").With("Negative", "<Keyboard>/t").With("Positive", "<Keyboard>/y");
		inputOverride.Enable();
	}

	private void OnDestroy()
	{
		inputOverride.Dispose();
	}

	public override void Activate()
	{
		AddRotation(0f - rotation);
		rotatorBase.localEulerAngles = new Vector3(0f, 0f, 0f);
		rotation = 0f;
	}

	public override void Deactivate()
	{
		AddRotation(0f - rotation);
		rotatorBase.localEulerAngles = new Vector3(0f, 0f, 0f);
		rotation = 0f;
	}

	public override void UpdatePart(PlaneContainer container)
	{
		float num = inputOverride.ReadValue<float>();
		float num2 = CustomMath.SnapToIncrement(Time.deltaTime * num * speed, 0.1f);
		rotation += num2;
		rotatorBase.localEulerAngles = new Vector3(0f, 0f, 0f - rotation);
		AddRotation(num2);
	}

	private void AddRotation(float rotation)
	{
		if (!Mathf.Approximately(rotation, 0f))
		{
			part.SetRotationRotator(Quaternion.AngleAxis(rotation, base.transform.forward * Mathf.Sign(base.transform.localScale.y)) * base.transform.rotation);
		}
	}

	public override PartStat[] GetPartStats()
	{
		return new PartStat[0];
	}

	public override void Save(GameDataWriter writer)
	{
		writer.Write(rotation);
		writer.Write(inputOverride.bindings[1].overridePath);
		writer.Write(inputOverride.bindings[2].overridePath);
	}

	public override void Load(GameDataReader reader)
	{
		rotation = reader.ReadFloat();
		string text = reader.ReadString();
		string text2 = reader.ReadString();
		if (!string.IsNullOrEmpty(text) && !string.IsNullOrWhiteSpace(text))
		{
			inputOverride.ApplyBindingOverride(1, text);
		}
		if (!string.IsNullOrEmpty(text2) && !string.IsNullOrWhiteSpace(text2))
		{
			inputOverride.ApplyBindingOverride(2, text2);
		}
	}
}
