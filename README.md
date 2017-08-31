add controller node
===================

- add node on fuel web
  
  - start node
  
  - set node network, disk on fuel web
  
  - add node on fuel web

- run add controller work flow with add controller node on fuel web

- run ansible add controller play book

  - set local
  
  - add controller play book

- run update controller work flow on fuel web

- check cloud services

delete controller node
======================

- delete node from fuel web

- run ansible update script

  - delete node from inventory/cloude_nodes

  - nginx update

- stop the delete node

- deploy controller update work flow from fuel web

- run ansible update script

  - init_master
  
  - local_master
  
  - update_controller

  - controller update
  
- delete node agent

- delete node from fuel
  ```
    fuel2 node undiscover --force -n node-id
  ```

- check cloude service
