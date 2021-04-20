# RBAC，基于用户角色的权限管理

## 用户，User

## 角色，Role
### 角色定义
- 访客，Guest
- 被锁定用户，Locked
- 普通用户，User
- 管理员，Administrator

## 权限，Permission
### 权限定义
- 查看权限，BROWSE
- 搜索权限，SEARCH
- 编辑权限，EDIT
- 创建权限，CREATE
- 删除权限，DELETE
- 管理员权限，ADMINISTER

## 关系

### 用户vs角色，一对多
- 一个用户只能是一种角色
- 一种角色可以有多个用户

### 角色vs权限，多对多
- 一种角色有多项权限
- 一项权限可以属于多个角色