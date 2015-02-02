s = 1; m = 1;
d = 3; w = 8*4+1;
{d - w ?
m = -m;
t = 1/d;
s = s + m*t;
d = d + 2;
}
< s; < N;
p = s;
m = -1; b = 1; n = 4*4; e = 1;
d = w; w = 8*8+1;
{d - w ?
m = -m;
t = 1/d;
s = s + m*t;
b = b*n/e;
< b; < N;  
p = p + s*b;
n = n-1; e = e+1;
d = d + 2;
}
p = p / 2^(2*7);
< p; < N;
$
