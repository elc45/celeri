

# The structure of the linear operator for the block model problem in `celeri`,

```math
\begin{bmatrix} 
    \mathbf{v} \\
    \boldsymbol{\omega}_\mathrm{c} \\
    \mathbf{s}_\mathrm{c} \\ 
    \mathbf{0} \\ 
    \mathbf{t}_\mathrm{c}(\mathrm{m}_1) \\ 
    \vdots \\ 
    \mathbf{0} \\ 
    \mathbf{t}_\mathrm{c}(\mathrm{m}_n) 
\end{bmatrix} 
=
\begin{bmatrix} 
    \mathbf{R}            & \mathbf{T}(\mathrm{m}_1) & \cdots & \mathbf{T}(\mathrm{m}_n) & \mathbf{E} & \mathbf{M} \\ 
    \mathbf{I}            & \mathbf{0}               & \cdots & \mathbf{0}               & \mathbf{0} & \mathbf{0} \\ 
    \mathbf{R}_\mathrm{s} & \mathbf{0}               & \cdots & \mathbf{0}               & \mathbf{0} & \mathbf{0} \\ 
    \mathbf{0}            & \mathbf{S}(\mathrm{m}_1) & \cdots & \mathbf{0}               & \mathbf{0} & \mathbf{0} \\ 
    \mathbf{0}            & \mathbf{I}               & \cdots & \mathbf{0}               & \mathbf{0} & \mathbf{0} \\ 
    \vdots                & \vdots                   & \ddots & \vdots                   & \vdots     & \vdots \\ 
    \mathbf{0}            & \mathbf{0}               & \cdots & \mathbf{S}(\mathrm{m}_n) & \mathbf{0} & \mathbf{0} \\ 
    \mathbf{0}            & \mathbf{0}               & \cdots & \mathbf{I}               & \mathbf{0} & \mathbf{0} 
\end{bmatrix} 
\begin{bmatrix} 
    \boldsymbol{\omega} \\ 
    \mathbf{t}(\mathrm{m}_1) \\ 
    \vdots \\ 
    \mathbf{t}(\mathrm{m}_n) \\ 
    \boldsymbol{\epsilon} \\ 
    \mathbf{m} 
\end{bmatrix}
```
