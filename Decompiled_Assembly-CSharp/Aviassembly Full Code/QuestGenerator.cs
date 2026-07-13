using System;
using System.Collections.Generic;
using UnityEngine;

public class QuestGenerator : Singleton<QuestGenerator>
{
	[Header("Input")]
	public float pricePerUnitOfCargo;

	public float weightPerUnitOfCargo;

	[Header("Quest generation test")]
	public CargoType cargoType;

	public int amount;

	[Space(10f)]
	public float estimatedCost;

	private CargoType[] allCargoTypes;

	[Header("Stat estimation")]
	public float maxSpeed;

	private bool initialized;

	private void Start()
	{
		allCargoTypes = Singleton<AirportManager>.Instance.allCargoTypes;
	}

	private void Update()
	{
		if (!initialized && (bool)Singleton<PlaneContainer>.Instance.gameObject.GetComponent<Rigidbody>())
		{
			initialized = true;
			EstimateStats();
		}
	}

	private void EstimateStats()
	{
		Rigidbody component = Singleton<PlaneContainer>.Instance.gameObject.GetComponent<Rigidbody>();
		float realGravity = Singleton<PlaneContainer>.Instance.RealGravity;
		Engine[] componentsInChildren = Singleton<PlaneContainer>.Instance.gameObject.GetComponentsInChildren<Engine>();
		Wing[] componentsInChildren2 = Singleton<PlaneContainer>.Instance.gameObject.GetComponentsInChildren<Wing>();
		for (float num = 0.25f; num < 45f; num += 0.25f)
		{
			float num2 = 0f;
			for (int i = 0; i < componentsInChildren.Length; i++)
			{
				num2 += componentsInChildren[i].GetMaxThrust(2000f);
			}
			float num3 = num2 / (component.mass * component.linearDamping);
			for (int j = 0; j < 100; j++)
			{
				num2 = 0f;
				for (int k = 0; k < componentsInChildren.Length; k++)
				{
					num2 += componentsInChildren[k].GetMaxThrust(num3);
				}
				float num4 = num2 * Mathf.Cos(num * (MathF.PI / 180f));
				float num5 = 0f;
				for (int l = 0; l < componentsInChildren2.Length; l++)
				{
					num5 += componentsInChildren2[l].GetDragForce(num3, num);
				}
				num3 = Mathf.Lerp((num4 - num5) / (component.mass * component.linearDamping), num3, Mathf.Min(0.5f, j));
			}
			float num6 = 0f;
			float num7 = num2 - num2 * Mathf.Cos(num * (MathF.PI / 180f));
			for (int m = 0; m < componentsInChildren2.Length; m++)
			{
				num6 += componentsInChildren2[m].GetLiftForce(num3, num, Singleton<PlaneContainer>.Instance);
			}
			if (num6 + num7 > realGravity * component.mass)
			{
				maxSpeed = num3;
				return;
			}
		}
		maxSpeed = -1f;
	}

	public DeliveryQuest GenerateDeliveryQuest(QuestDifficulty questDifficulty, Airport airport)
	{
		float money = Singleton<MoneyManager>.Instance.money;
		float num = 1f + (float)questDifficulty * 0.15f;
		List<CargoType> list = new List<CargoType>();
		for (int i = 0; i < allCargoTypes.Length; i++)
		{
			if (EstimateCost(allCargoTypes[i], 1) / money < num && (airport.cargoType == null || airport.cargoType.Length == 0 || allCargoTypes[i] != airport.cargoType[0]))
			{
				list.Add(allCargoTypes[i]);
			}
		}
		CargoType cargoType = list[UnityEngine.Random.Range(0, list.Count)];
		int num2 = 1;
		for (int j = 1; j < 1000; j++)
		{
			if (EstimateCost(cargoType, j) / money > num - 0.05f)
			{
				num2 = j;
				break;
			}
		}
		DeliveryQuestData deliveryQuestData = ScriptableObject.CreateInstance<DeliveryQuestData>();
		deliveryQuestData.name = "Deliver[amount][cargoType]";
		deliveryQuestData.cargoType = cargoType;
		deliveryQuestData.amount = num2;
		deliveryQuestData.description = "";
		deliveryQuestData.completeMessage = "";
		deliveryQuestData.giveMessage = "";
		return (DeliveryQuest)deliveryQuestData.CreateQuest(airport);
	}

	private float EstimateCost(CargoType cargoType, int amount)
	{
		return Mathf.Pow(cargoType.cargoSpace * amount, 1.65f);
	}
}
