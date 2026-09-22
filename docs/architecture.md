# Software Architecture

## 1. Software Description

## 2. Architecture Overview

## 3. Monitoring Microservice

## 4. Inference Microservice

## 5. PostgreSQL Database

## 6. REST Communication

## 7. Kubernetes Service Discovery

## 8. External Access

## 9. Horizontal Scaling

## 10. Persistent Storage

## 11. Self-Healing

## 12. Component-to-Microservice Mapping

Browser
   |
   v
NodePort :30081
   |
   v
Monitoring Service
   |
   +------ REST ------> Inference Service
   |                        |
   |                        v
   |                 Logistic Regression
   |
   +------ SQL -------> PostgreSQL Service
                            |
                            v
                       PostgreSQL Pod
                            |
                            v
                    PersistentVolumeClaim