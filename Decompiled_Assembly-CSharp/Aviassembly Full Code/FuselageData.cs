public struct FuselageData(float cargoVolume, float mass, float price, float volume)
{
	public float cargoVolume = cargoVolume;

	public float mass = mass;

	public float price = price;

	public float volume = volume;

	public FuselageData ChangeVolume(float newVolume)
	{
		float num = cargoVolume / volume * newVolume;
		float num2 = mass / volume * newVolume;
		float num3 = price / volume * newVolume;
		return new FuselageData(num, num2, num3, newVolume);
	}
}
