using System;

namespace Basement
{
	public class RandomKeyExpander : IKeyExpander<int>
	{
		public RandomKeyExpander() { }

		public int[] Expand(int key, int length)
		{
			var random = new Random(key);
			var expandedKey = new int[length];

			for (var i = 0; i < expandedKey.Length; i++)
				expandedKey[i] = random.Next();

			return expandedKey;
		}
	}
}
