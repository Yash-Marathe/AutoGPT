class Stack<T> {
  final List<T> _list = [];

  void push(T element) {
    _list.add(element);
  }

  T pop() {
    if (isEmpty) {
      throw StateError('Cannot pop from an empty stack');
    }
    var element = _list.last;
    _list.removeLast();
    return element;
  }

  T peek() {
    if (isEmpty) {
      throw StateError('Cannot peek at an empty stack');
    }
    return _list.last;
  }

  bool get isEmpty => _list.isEmpty;
  bool get isNotEmpty => _list.isNotEmpty;

  int get length => _list.length;

  void clear() {
    _list.clear();
  }

  @override
  String toString() {
    return 'Stack(${_list.join(', ')})';
  }
}
