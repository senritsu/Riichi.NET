using System;
using System.Linq;

namespace RiichiSharp.Domain
{
    public static class TileExtensions
    {
        public static bool IsHonor(this Tile tile)
        {
            return TileGroup.Honors.Contains(tile);
        }

        public static bool IsNumeric(this Tile tile)
        {
            return !tile.IsHonor();
        }

        public static bool IsSimple(this Tile tile)
        {
            return TileGroup.Simples.Contains(tile);
        }

        public static bool IsTerminal(this Tile tile)
        {
            return TileGroup.Terminals.Contains(tile);
        }

        public static Suit Suit(this Tile tile)
        {
            if (tile < Tile.Pin1 || tile > Tile.Chun)
            {
                throw new ArgumentOutOfRangeException("tile", "Invalid tile value");
            }
            foreach (var suit in Enum.GetValues(typeof(Suit)).Cast<Suit>())
            {
                if ((int)tile < (int)suit)
                {
                    return suit;
                }
            }
            throw new IndexOutOfRangeException("Tile value inside bounds, but no suit found");
        }

        public static Tile Shift(this Tile tile, int shift)
        {
            var suit = tile.Suit();

            int mod;
            switch (suit)
            {
                case Domain.Suit.Kazehai:
                    mod = 4;
                    break;
                case Domain.Suit.Sangenpai:
                    mod = 3;
                    break;
                default:
                    mod = 9;
                    break;
            }

            var offset = (int)suit - mod;
            var x = (int)tile - offset + shift;

            return (Tile)(offset + (shift < 0 ? ((x % mod) + mod) % mod : x % mod));
        }

        public static Tile Next(this Tile tile)
        {
            return tile.Shift(1);
        }

        public static Tile Previous(this Tile tile)
        {
            return tile.Shift(-1);
        }

        public static bool CanFormSequence(this Tile tile)
        {
            return (int)tile < (int)Domain.Suit.Manzu;
        }
    }
}
