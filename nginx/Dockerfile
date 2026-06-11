FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf
COPY switch.sh /switch.sh
RUN chmod +x /switch.sh

CMD sh -c "nginx && /switch.sh"
