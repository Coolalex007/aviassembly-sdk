using UnityEngine.InputSystem;

public class Decoupler : PlanePart
{
	public InputAction inputOverride;

	private BuildingPart part;

	private void Awake()
	{
		part = GetComponent<BuildingPart>();
		inputOverride = new InputAction("ThrottleInput");
		inputOverride.AddBinding("<Keyboard>/h");
		inputOverride.Enable();
	}

	private void OnDestroy()
	{
		inputOverride.Dispose();
	}

	public override void UpdatePart(PlaneContainer container)
	{
		if (inputOverride.triggered)
		{
			Decouple();
		}
	}

	private void Decouple()
	{
		for (int i = 0; i < part.children.Count; i++)
		{
			Singleton<PartExploder>.Instance.ExplodePart(part.children[i].gameObject.GetComponentInChildren<PlanePart>(), rootExplosion: true, disableExplosion: true);
		}
	}

	public override PartStat[] GetPartStats()
	{
		return new PartStat[0];
	}

	public override void Save(GameDataWriter writer)
	{
		writer.Write(inputOverride.bindings[0].overridePath);
	}

	public override void Load(GameDataReader reader)
	{
		string text = reader.ReadString();
		if (!string.IsNullOrEmpty(text))
		{
			inputOverride.ApplyBindingOverride(0, text);
		}
	}
}
