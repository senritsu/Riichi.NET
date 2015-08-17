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

using System;
using System.Collections;
using System.Collections.Generic;

namespace RiichiSharp.Utilities
{
    public class PlayerSpecificValue<T> where T : struct
    {
        private readonly T[] _contents = new T[4];

        public T this[int index]
        {
            get
            {
                if (index < 0 || index > 3)
                {
                    throw new IndexOutOfRangeException();
                }
                return _contents[index];
            }
            set
            {
                if (index < 0 || index > 3)
                {
                    throw new IndexOutOfRangeException();
                }
                _contents[index] = value;
            }
        }
    }

    public interface IPlayerSpecificReadOnlyCollection<out T>
    {
        IReadOnlyList<T> this[int index] { get; }
    }

    public class PlayerSpecificCollection<T> : IPlayerSpecificReadOnlyCollection<T>
    {
        private readonly List<T>[] _contents = new List<T>[4];

        public PlayerSpecificCollection()
        {
            for (int i = 0; i < 4; i++)
            {
                _contents[i] = new List<T>();
            }
        }

        IReadOnlyList<T> IPlayerSpecificReadOnlyCollection<T>.this[int index]
        {
            get { return this[index]; }
        }

        public List<T> this[int index]
        {
            get
            {
                if (index < 0 || index > 3)
                {
                    throw new IndexOutOfRangeException();
                }
                return _contents[index];
            }
        }
    }

    public class PlayerSpecificObject<T> : IEnumerable<T>
    {
        private readonly IList<T> _contents = new T[4];

        public PlayerSpecificObject(T first, T second, T third, T fourth)
        {
            _contents[0] = first;
            _contents[1] = second;
            _contents[2] = third;
            _contents[3] = fourth;
        }

        public virtual T this[int index]
        {
            get
            {
                if (index < 0 || index > 3)
                {
                    throw new IndexOutOfRangeException();
                }
                return _contents[index];
            }
        }

        public IEnumerator<T> GetEnumerator()
        {
            return _contents.GetEnumerator();
        }

        IEnumerator IEnumerable.GetEnumerator()
        {
            return GetEnumerator();
        }
    }

    public class PlayerSpecificObjectWithDefault<T> : PlayerSpecificObject<T> where T : new()
    {
        private readonly T[] _contents = new T[4];

        public PlayerSpecificObjectWithDefault()
            : base(new T(), new T(), new T(), new T())
        {
        }

        public override T this[int index]
        {
            get
            {
                if (index < 0 || index > 3)
                {
                    throw new IndexOutOfRangeException();
                }
                return _contents[index];
            }
        }
    }
}
