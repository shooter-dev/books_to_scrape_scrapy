# API Statistics Endpoints Documentation

## 📊 Nouvelles Routes de Statistiques / New Statistics Routes

Toutes les routes de statistiques sont préfixées par `/stats` et retournent les prix en **centimes** ET en **euros**.

All statistics routes are prefixed with `/stats` and return prices in both **cents** AND **euros**.

---

## Endpoints Disponibles / Available Endpoints

### 1. **Prix Moyen / Average Price**
```http
GET /stats/average-price
```

**Description:**
Calcule le prix moyen de tous les livres du catalogue.
Calculate the average price of all books in the catalog.

**Response:**
```json
{
  "message": "Prix moyen calculé avec succès",
  "data": {
    "average_price_cents": 3824,
    "average_price_euros": 38.24
  }
}
```

---

### 2. **Fourchette de Prix / Price Range**
```http
GET /stats/price-range
```

**Description:**
Retourne les prix minimum et maximum du catalogue.
Return minimum and maximum prices in the catalog.

**Response:**
```json
{
  "message": "Fourchette de prix récupérée avec succès",
  "data": {
    "min_price_cents": 1000,
    "min_price_euros": 10.00,
    "max_price_cents": 5999,
    "max_price_euros": 59.99
  }
}
```

---

### 3. **Top Catégories / Top Categories**
```http
GET /stats/top-categories?limit=10
```

**Description:**
Retourne les catégories avec le plus de livres.
Return categories with the most books.

**Query Parameters:**
- `limit` (optional, default=10, max=50): Nombre de catégories à retourner / Number of categories to return

**Response:**
```json
{
  "message": "Top catégories récupérées avec succès",
  "data": {
    "top_categories": [
      {
        "category": "Fiction",
        "count": 245
      },
      {
        "category": "Mystery",
        "count": 189
      },
      {
        "category": "Science Fiction",
        "count": 156
      }
    ],
    "total_returned": 3
  }
}
```

---

### 4. **Distribution des Notes / Rating Distribution**
```http
GET /stats/rating-distribution
```

**Description:**
Retourne la distribution des notes avec pourcentages.
Return rating distribution with percentages.

**Response:**
```json
{
  "message": "Distribution des notes récupérée avec succès",
  "data": {
    "distribution": [
      {
        "rating": "Five",
        "count": 342,
        "percentage": 34.2
      },
      {
        "rating": "Four",
        "count": 289,
        "percentage": 28.9
      },
      {
        "rating": "Three",
        "count": 215,
        "percentage": 21.5
      },
      {
        "rating": "Two",
        "count": 103,
        "percentage": 10.3
      },
      {
        "rating": "One",
        "count": 51,
        "percentage": 5.1
      }
    ],
    "total_books": 1000
  }
}
```

---

### 5. **Statistiques par Catégorie / Category Statistics**
```http
GET /stats/category/{category_name}
```

**Description:**
Retourne des statistiques détaillées pour une catégorie spécifique.
Return detailed statistics for a specific category.

**Path Parameters:**
- `category_name` (required): Nom de la catégorie / Category name

**Example:**
```http
GET /stats/category/Fiction
```

**Response:**
```json
{
  "message": "Statistiques de la catégorie 'Fiction' récupérées avec succès",
  "data": {
    "category": "Fiction",
    "total_books": 245,
    "avg_price": 3456,
    "avg_price_euros": 34.56,
    "min_price": 1200,
    "min_price_euros": 12.00,
    "max_price": 5890,
    "max_price_euros": 58.90
  }
}
```

**Error Responses:**
- `404 Not Found`: Catégorie non trouvée ou vide / Category not found or empty

---

### 6. **Statistiques Globales / Overall Statistics**
```http
GET /stats/overall
```

**Description:**
Retourne toutes les statistiques globales du catalogue en un seul appel.
Return all overall catalog statistics in a single call.

**Response:**
```json
{
  "message": "Statistiques globales récupérées avec succès",
  "data": {
    "total_books": 1000,
    "total_categories": 52,
    "avg_price": 3824,
    "avg_price_euros": 38.24,
    "min_price": 1000,
    "min_price_euros": 10.00,
    "max_price": 5999,
    "max_price_euros": 59.99
  }
}
```

---

## 🔧 Architecture Technique / Technical Architecture

Ces endpoints suivent l'architecture **DDD (Domain-Driven Design)** :

These endpoints follow **DDD (Domain-Driven Design)** architecture:

```
Routes (API Layer)
    ↓
Use Cases (Application Layer)
    ↓
Services (Domain Layer)
    ↓
Repositories (Infrastructure Layer)
    ↓
Database (PostgreSQL)
```

### Fichiers Modifiés / Modified Files:

1. **`repositories/book_repository.py`**
   - Ajout de 6 méthodes de statistiques SQL / Added 6 SQL statistics methods

2. **`services/book_service.py`**
   - Ajout de la logique métier avec conversion centimes→euros / Added business logic with cents→euros conversion

3. **`use_cases/book_use_case.py`**
   - Ajout de 6 use cases avec gestion d'erreurs / Added 6 use cases with error handling

4. **`routes/stats_route.py`** (nouveau / new)
   - Création de 6 endpoints REST / Created 6 REST endpoints

5. **`main.py`**
   - Inclusion du router de statistiques / Included statistics router

---

## 💰 Gestion des Prix / Price Management

**Important:** Les prix sont stockés en **centimes (INTEGER)** dans la base de données pour éviter les erreurs d'arrondi.

Prices are stored as **cents (INTEGER)** in the database to avoid rounding errors.

### Exemple / Example:
- **BDD:** `4517` centimes
- **API Response:**
  - `price_cents: 4517`
  - `price_euros: 45.17`

---

## 📚 Documentation Interactive / Interactive Documentation

Accédez à la documentation Swagger pour tester les endpoints :

Access Swagger documentation to test endpoints:

```
http://localhost:8000/docs
```

ou / or

```
http://localhost:8000/redoc
```

---

## ✅ Status Codes

| Code | Description |
|------|-------------|
| `200` | Succès / Success |
| `400` | Erreur de validation / Validation error |
| `404` | Ressource non trouvée / Resource not found |
| `500` | Erreur serveur / Server error |

---

## 🚀 Exemple d'Utilisation / Usage Example

```bash
# Prix moyen
curl -X GET "http://localhost:8000/stats/average-price"

# Top 5 catégories
curl -X GET "http://localhost:8000/stats/top-categories?limit=5"

# Statistiques d'une catégorie
curl -X GET "http://localhost:8000/stats/category/Fiction"

# Statistiques globales
curl -X GET "http://localhost:8000/stats/overall"
```

---

**Version:** 1.0.0
**Date:** 2025-10-03
