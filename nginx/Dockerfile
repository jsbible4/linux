#최신 버전의 nginx이미지를 기반으로 사용.
FROM nginx:latest   

#nginx 설정 파일을 컨테이너의 위치로 복사.
COPY default.conf /etc/nginx/conf.d/default.conf  

#html폴더의 모든 내용을 컨테이너의 nginx html 디렉토리로 복사.
COPY html/ /usr/share/nginx/html/   
