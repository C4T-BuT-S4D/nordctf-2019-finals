using System;
using System.IO;
using System.Text;

namespace Basement
{
	public class Program
	{
		public static void Main(string[] args)
		{
			int key;

			if (args.Length < 4 || !int.TryParse(args[1], out key))
				return;

			var encrypter = GetEncrypter(key);
			var data = File.ReadAllBytes(args[2]);

			switch (args[0]) 
			{
				case "encrypt":
					File.WriteAllBytes(args[3], encrypter.Encrypt(key, data));
					break;
				case "decrypt":
					File.WriteAllBytes(args[3], encrypter.Decrypt(key, data));
					break;
			}
		}

		protected static IEncrypter<int> GetEncrypter(int key)
		{
			var bytesCoder = new Base64BytesCoder(Encoding.UTF8);
			var arrayPacker = new ByteIntArrayPacker();
			var keyExpander = new RandomKeyExpander();
			return new XorEncrypter(bytesCoder, arrayPacker, keyExpander);
		}
	}
}
