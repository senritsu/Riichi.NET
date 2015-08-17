/***************************************************************************\
The MIT License (MIT)

Copyright (c) 2015 Jonas Schiegl (https://github.com/senritsu)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
\***************************************************************************/

using System.Collections.Generic;
using RiichiSharp.Enums;

namespace RiichiSharp.Analysis
{
    public partial class YakuDetails
    {
        public static Dictionary<Yaku, YakuDetails> Data = new Dictionary<Yaku, YakuDetails>
        {
            { Yaku.Riichi, new YakuDetails { Yaku = Yaku.Riichi, Value = 1, Name = "Riichi" } },
            { Yaku.MenzenTsumo, new YakuDetails { Yaku = Yaku.MenzenTsumo, Value = 1, Name = "Menzen Tsumo" } },
            { Yaku.Ippatsu, new YakuDetails { Yaku = Yaku.Ippatsu, Value = 1, Name = "Ippatsu" } },
            { Yaku.Chankan, new YakuDetails { Yaku = Yaku.Chankan, Value = 1, Name = "Chankan" } },
            { Yaku.RinshanKaihou, new YakuDetails { Yaku = Yaku.RinshanKaihou, Value = 1, Name = "Rinshan Kaihou" } },
            { Yaku.HaiteiRaoyue, new YakuDetails { Yaku = Yaku.HaiteiRaoyue, Value = 1, Name = "Haitei Raoyue" } },
            { Yaku.HouteiRaoyui, new YakuDetails { Yaku = Yaku.HouteiRaoyui, Value = 1, Name = "Houtei Raoyui" } },
            { Yaku.Pinfu, new YakuDetails { Yaku = Yaku.Pinfu, Value = 1, Name = "Pinfu" } },
            { Yaku.Iipeikou, new YakuDetails { Yaku = Yaku.Iipeikou, Value = 1, Name = "Iipeikou" } },
            { Yaku.TanYao, new YakuDetails { Yaku = Yaku.TanYao, Value = 1, Name = "Tan'yao" } },
            { Yaku.Yakuhai, new YakuDetails { Yaku = Yaku.Yakuhai, Value = 1, Name = "Yakuhai" } },
            { Yaku.Kazepai, new YakuDetails { Yaku = Yaku.Kazepai, Value = 1, Name = "Kazepai" } },

            { Yaku.DabuRii, new YakuDetails { Yaku = Yaku.DabuRii, Value = 2, Name = "Double Riichi" } },
            { Yaku.OpenRiichi, new YakuDetails { Yaku = Yaku.OpenRiichi, Value = 2, Name = "Open Riichi" } },
            { Yaku.Dabukaze, new YakuDetails { Yaku = Yaku.Dabukaze, Value = 2, Name = "Dabukaze" } },
            { Yaku.ChiiToitsu, new YakuDetails { Yaku = Yaku.ChiiToitsu, Value = 2, Name = "ChiiToitsu" } },
            { Yaku.SanshokuDoujun, new YakuDetails { Yaku = Yaku.SanshokuDoujun, Value = 2, Name = "Sanshoku Doujun" } },
            { Yaku.Ittsuu, new YakuDetails { Yaku = Yaku.Ittsuu, Value = 2, Name = "Ittsuu" } },
            { Yaku.Toitoi, new YakuDetails { Yaku = Yaku.Toitoi, Value = 2, Name = "Toitoi" } },
            { Yaku.SanshokuDoukou, new YakuDetails { Yaku = Yaku.SanshokuDoukou, Value = 2, Name = "Sanshoku Doukou" } },
            { Yaku.SanAnkou, new YakuDetails { Yaku = Yaku.SanAnkou, Value = 2, Name = "San Ankou" } },
            { Yaku.SanKantsu, new YakuDetails { Yaku = Yaku.SanKantsu, Value = 2, Name = "San Kantsu" } },
            { Yaku.Chanta, new YakuDetails { Yaku = Yaku.Chanta, Value = 2, Name = "Chanta" } },

            { Yaku.HonItsu, new YakuDetails { Yaku = Yaku.HonItsu, Value = 3, Name = "Hon'itsu" } },
            { Yaku.Junchan, new YakuDetails { Yaku = Yaku.Chanta, Value = 3, Name = "Junchan" } },
            { Yaku.Ryanpeikou, new YakuDetails { Yaku = Yaku.Chanta, Value = 3, Name = "Ryanpeikou" } },

            { Yaku.Honrou, new YakuDetails { Yaku = Yaku.Honrou, Value = 4, Name = "Honrou" } },
            { Yaku.Shousangen, new YakuDetails { Yaku = Yaku.Shousangen, Value = 4, Name = "Shousangen" } },

            { Yaku.ChinItsu, new YakuDetails { Yaku = Yaku.ChinItsu, Value = 6, Name = "Kazepai" } },

            { Yaku.Tenhou, new YakuDetails { Yaku = Yaku.Tenhou, Value = 13, Name = "Tenhou" } },
            { Yaku.Chihou, new YakuDetails { Yaku = Yaku.Chihou, Value = 13, Name = "Chihou" } },
            { Yaku.Renhou, new YakuDetails { Yaku = Yaku.Renhou, Value = 13, Name = "Renhou" } },
            { Yaku.KokushiMusou, new YakuDetails { Yaku = Yaku.KokushiMusou, Value = 13, Name = "Kokushi Musou" } },
            { Yaku.ChuurenPoutou, new YakuDetails { Yaku = Yaku.ChuurenPoutou, Value = 13, Name = "Chuuren Poutou" } },
            { Yaku.SuuAnkou, new YakuDetails { Yaku = Yaku.SuuAnkou, Value = 13, Name = "Suu Ankou" } },
            { Yaku.Daisangen, new YakuDetails { Yaku = Yaku.Daisangen, Value = 13, Name = "Daisangen" } },
            { Yaku.Shousuushi, new YakuDetails { Yaku = Yaku.Shousuushi, Value = 13, Name = "Shousuushi" } },
            { Yaku.SuuKantsu, new YakuDetails { Yaku = Yaku.SuuKantsu, Value = 13, Name = "Suu Kantsu" } },
            { Yaku.Ryuuisou, new YakuDetails { Yaku = Yaku.Ryuuisou, Value = 13, Name = "Ryuuisou" } },
            { Yaku.Tsuuisou, new YakuDetails { Yaku = Yaku.Tsuuisou, Value = 13, Name = "Tsuuisou" } },
            { Yaku.Chinroutou, new YakuDetails { Yaku = Yaku.Chinroutou, Value = 13, Name = "Chinroutou" } },
            { Yaku.Daisharin, new YakuDetails { Yaku = Yaku.Daisharin, Value = 13, Name = "Daisharin" } },

            { Yaku.KokushiMusou13SidedWait, new YakuDetails { Yaku = Yaku.KokushiMusou13SidedWait, Value = 14, Name = "Kokushi Musou (13-sided wait)" } },
            { Yaku.ChuurenPoutou9SidedWait, new YakuDetails { Yaku = Yaku.ChuurenPoutou9SidedWait, Value = 14, Name = "Chuuren Poutou (9-sided wait)" } },
            { Yaku.Daisuushi, new YakuDetails { Yaku = Yaku.Daisuushi, Value = 14, Name = "Daisuushi" } },
            { Yaku.Daichisei, new YakuDetails { Yaku = Yaku.Daichisei, Value = 14, Name = "Daichisei" } },
            { Yaku.Paarenchan, new YakuDetails { Yaku = Yaku.Paarenchan, Value = 14, Name = "Paarenchan" } },
        };
    }
}
