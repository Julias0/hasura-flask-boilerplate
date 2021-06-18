How to setup auto metadata application + migrations - 
First time
- installation of local hasura cli
- run docker-compose with either cli or non-cli image
- configure data settings (which tables to track) inside hasura console
- on local side, run hasura init hasura --endpoint http://localhost:8080 
To setup up metadata - 
- on local side, ruin cd hasura; hasura metadata export --admin-secret=AkkiBarModiSarkar
- make sure the local metadata dir is mapped to /hasura-metadata on the hasura cli image
- bring docker-compose up and down and will and state of metadata persists