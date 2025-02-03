# korona

Why does romantizer really matter?

-   ko->ro: good for teach korean to engl-ish culture or get great name for project.
-   ro->ko: prevent korea citizen from blaming too seriously in korean-cypher.(which o1 can actually understand)

### How to start?

```
pip install korokoro
```

ko->ro

```python
from korokoro import Romanizer
Romanizer("안녕").romanize() # annyeong
```

ro->ko

```python
from korokoro import Koreanizer
# Not implemented
```

### Neat Technical Hack

-   ko->ro: just following `korean.go.kr`'s textbook
-   ro->ko: probably hard (e.g. sarang -> 사랑 or 살앙)
