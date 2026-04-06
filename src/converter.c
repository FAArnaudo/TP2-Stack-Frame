extern long to_int(float r1, float r2, float r3, float r4, float r5, float r6,
                   float r7, float r8, float a);
extern int plus_one(int r1, int r2, int r3, int r4, int r5, int r6, int a);

int to_int_plus_one(float numb_float) {
  int result =
      to_int(0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, numb_float);
  return plus_one(0, 0, 0, 0, 0, 0, result);
}
