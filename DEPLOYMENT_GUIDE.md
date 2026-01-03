# UHIP Deployment Guide

## Overview
This guide covers deployment strategies for the Unified Hybrid Intelligence Platform (UHIP) in various environments: development, staging, and production.

## Prerequisites
- Docker and Docker Compose installed
- Kubernetes cluster (for production)
- Cloud provider credentials (AWS, Azure, or GCP)
- Python 3.9+ environment
- Terraform (for Infrastructure as Code)

## Local Development Deployment

### Using Docker Compose
```bash
docker-compose up -d
```

This starts all services locally including:
- UHIP API server
- Database (PostgreSQL)
- Cache (Redis)
- Message queue (RabbitMQ)

### Accessing Services
- API: http://localhost:8000
- Admin Panel: http://localhost:8001
- Database: localhost:5432

## Staging Deployment

### Using Docker
```bash
# Build image
docker build -t uhip:staging .

# Run with environment variables
docker run -e ENV=staging -p 8000:8000 uhip:staging
```

### Environment Configuration
Create `.env.staging` file:
```
ENV=staging
DATABASE_URL=postgresql://user:pass@staging-db:5432/uhip
REDIS_URL=redis://staging-redis:6379
LOG_LEVEL=INFO
```

## Production Deployment

### Kubernetes Deployment

1. Build and push image:
```bash
docker build -t your-registry/uhip:v1.0.0 .
docker push your-registry/uhip:v1.0.0
```

2. Apply Kubernetes manifests:
```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

3. Verify deployment:
```bash
kubectl get pods -n uhip
kubectl logs -n uhip deployment/uhip
```

### Auto-Scaling
Enable Horizontal Pod Autoscaling:
```bash
kubectl autoscale deployment uhip -n uhip --min=3 --max=10
```

### Cloud Provider Specific

#### AWS Deployment
```bash
# Using ECS
aws ecs create-service --cluster production --service-name uhip --task-definition uhip:1

# Using EKS
export KUBECONFIG=$(aws eks update-kubeconfig --name uhip-prod --region us-east-1)
kubectl apply -f k8s/
```

#### Azure Deployment
```bash
# Using AKS
az aks get-credentials --resource-group uhip-prod --name uhip-aks
kubectl apply -f k8s/

# Using Container Instances
az container create --resource-group uhip-prod --name uhip-app
```

#### GCP Deployment
```bash
# Using GKE
gcloud container clusters get-credentials uhip-prod
kubectl apply -f k8s/

# Using Cloud Run
gcloud run deploy uhip --image uhip:latest --region us-central1
```

## Database Migrations

### Running Migrations
```bash
alembic upgrade head
```

### Rollback
```bash
alembic downgrade -1
```

## Health Checks

### API Health Endpoint
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy", "timestamp": "2026-01-03T10:00:00Z"}
```

## Monitoring and Logging

### Using Prometheus
```yaml
scrape_configs:
  - job_name: 'uhip'
    static_configs:
      - targets: ['localhost:8000']
```

### Using ELK Stack
- Elasticsearch: For storing logs
- Logstash: For processing logs
- Kibana: For visualization

## Backup and Recovery

### Database Backup
```bash
pg_dump -U postgres uhip_db > backup.sql
```

### Restore from Backup
```bash
psql -U postgres -d uhip_db < backup.sql
```

## Performance Optimization

- Enable caching: Configure Redis for session and data caching
- Database optimization: Create indexes on frequently queried columns
- Load balancing: Distribute traffic across multiple instances
- CDN: Use CDN for static assets

## Troubleshooting

### Common Issues

1. **Service won't start**
   - Check logs: `docker logs container-id`
   - Verify environment variables
   - Check port availability

2. **Database connection fails**
   - Verify DATABASE_URL
   - Check database service is running
   - Verify network connectivity

3. **High memory usage**
   - Check for memory leaks
   - Adjust container memory limits
   - Review application logs

## Security Considerations

- Use HTTPS only in production
- Implement rate limiting
- Set up WAF (Web Application Firewall)
- Enable audit logging
- Regular security patches and updates

## Support
For deployment issues, refer to DEVELOPER_README.md or open a GitHub issue.
