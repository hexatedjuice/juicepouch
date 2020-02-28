## hackthebox - da vinci (30)

- stego
- by nickvourd

files:
- monalisa.jpg
- Plans.jpg
- Thepassword_is_the_small_name_of_the_actor_named_Hanks.jpg

first we can go for the low hanging fruit using ```strings```

```
$ strings monalisa.jpg | grep '.\{10,12\}'
;CREATOR: gd-jpeg v1.0 (using IJG JPEG v62), quality = 92
5Optimized by JPEGmini 3.9.20.0L Internal 0x8c97c7da
 /2.)2&*+)

...

NhY`&<kwl3
FayU)W^[Ja=
6$}%U.cU(s
Mona.jpgUT
famous.zipUT
```
we see that there is a zip file embedded in monalisa.jpg. we'll come back to that later

```
$ strings Plans.jpg | grep '.\{10,12\}'
//33//@@@@@@@@@@@@@@@
#0+.'''.+550055@@?@@@@@@@@@@@@
?:Vn.$R0!B@X2
rLXn0~uHg*T
zS?jh_{3&!
nI"L(oK'b4
zX^(1*cxY3:
(CDRYFLD8,
https://www.youtube.com/watch?v=jc1Nfx4c5LQ
```
there seems to be a youtube link in Plans.jpg. it leads to a video titled "Guernica 3D".

i didn't see anything noteworthy in Thepassword_is_the_small_name_of_the_actor_named_Hanks.jpg from using strings


