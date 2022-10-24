# `normal_and_tangent_to_orientation`

Converts two vectors to an orientation. This is similar to an aim constraint, where one functions as an "aim" and the other as an "up" vector. 

## Prioritize normal

This orientation aligns the Y axis along the normal and the local Z axis along the tangent. If the vectors are not exactly orthogonal, `prioritize_normal` controls which one is prioritized. 

`prioritize_normal` means the Y axis / normal are exactly aligned and Z axis / tangent are aligned as closely as possible. If off, the Y axis / normal are aligned as closely as possible, and the Z axis / tangent are exactly aligned. 