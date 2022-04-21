class ECC {
  late int p;
  late int a;
  late int b;
  List<dynamic> id = ["Point at infinity", "Point at infinity"];

  ECC(int p, int a, int b) {
    this.p = p;
    this.a = a;
    this.b = b;
  }

  int power(int x, int n) {
    int retval = 1;
    for (int i = 0; i < n; i++) {
      retval *= x;
    }
    return retval;
  }

  bool checkPoint(p) {
    if (p != this.id) {
      var ls = (p[1] * p[1]) % this.p;
      var hs = ((power(p[0], 3)) + (this.a * p[0]) + this.b) % this.p;
      if (ls == hs)
        return true;
      else
        return false;
    } else
      return true;
  }

  multiplumOfPoint(p, n) {
    print(n);
    if (checkPoint(p)) {
      var first = p;
      var second = calcPoint(p, p, lambdaEqual(p));
      var res = second;

      if (n == 1)
        return first;
      else if (n == 2)
        return second;
      else {
        for (int i = 2; i < n; i++) {
          res = addPoints(first, res);
        }
      }

      return res;
    }
  }

  addPoints(p1, p2) {
    if (checkPoint(p1) && checkPoint(p2)) {
      if (p1 == this.id) {
        return p2;
      } else if (p2 == this.id)
        return p1;
      else if (p1[0] == p2[0] && p1[1] == ((-p2[1]) % this.p))
        return this.id;
      else if (p1[0] == p2[0] && p1[1] == p2[1])
        return calcPoint(p1, p2, lambdaEqual(p1));
      else
        return calcPoint(p1, p2, lambdaDiff(p1, p2));
    }
  }

  inversePoint(p) {
    if (checkPoint(p) && (p != id)) {
      return [p[0], ((-p[1]) % this.p)];
    } else if (p == id) return p;
  }

  calcPoint(p1, p2, l) {
    var x = ((l * l) - p1[0] - p2[0]) % this.p;
    var y = ((l * (p1[0] - x)) - p1[1]) % this.p;
    return [x, y];
  }

  lambdaEqual(p1) {
    var l =
        ((3 * p1[0] * p1[0]) + this.a) * (modinv((2 * p1[1]), this.p)) % this.p;
    return l;
  }

  lambdaDiff(p1, p2) {
    var l =
        (p2[1] - p1[1]) * (modinv(((p2[0] - p1[0]) % this.p), this.p)) % this.p;
    return l;
  }

  egcd(a, b) {
    if (a == 0)
      return [b, 0, 1];
    else {
      var res = egcd(b % a, a);
      return [res[0], res[2] - (b ~/ a) * res[1], res[1]];
    }
  }

  modinv(a, m) {
    var res = egcd(a, m);

    if (res[0] == 1) return res[1] % m;
  }
}
