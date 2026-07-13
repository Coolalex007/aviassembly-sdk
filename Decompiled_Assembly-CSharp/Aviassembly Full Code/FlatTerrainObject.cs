using UnityEngine;

public struct FlatTerrainObject(Vector3 worldPos, FlatnessRectangle rectangle2D, float height, float blendingDistance)
{
	public Vector3 worldPos = worldPos;

	public FlatnessRectangle rectangle2D = rectangle2D;

	public float blendingDistance = blendingDistance;

	public float height = height;
}
