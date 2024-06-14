# PS visio - video reencoder
## Sobre
Este é um desafio proposto pela Visio para sua vaga de estágio em infraestrutura. O objetivo é comparar estratégias de reencode de vídeo para reduzir custos.
Para isso, são propostos 3 encoders que se pode gravar os vídeos (H264. H264+ e H265) e três encoders que se pode fazer o reencode (VP8, VP9 e AV1), e deve-se
comparar o custo desse processamento (em min) e o custo em armazenamento (em mb).
Por fim, deve-se propor uma API que realizará esse processo de maneira automática

## Como rodar
1. Tenha o [docker instalado](https://docs.docker.com/engine/install/)
2. Builde a image
```sh
docker build . -t video_reencoder
```
3. Rode seu container.
Monte uma pasta de seu computador ao container para que ele possa ter acesso aos vídeos de origem.

Passe como variável de ambiente o path do arquivo nesse mount ou volume (INPUT_FILE_PATH), e também o tipo de encode destino (ENCODE_DST), que pode ser VP8, VP9, OU AV1

Exemplo:

```sh
docker run -it --mount type=bind,src=./videos/,dst=/home/videos -e INPUT_FILE_PATH=videos/video1.mp4 -e ENCODE_DST=AV1 ffmpeg-decoder
```
