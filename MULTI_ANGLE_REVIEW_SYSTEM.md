# Multi-Angle Product Image Upload & Review System

## New Features Added

### 1. Multi-Angle Image Upload

Users can now upload product images from 5 different angles:
- **Front** - Front facing label
- **Back** - Back of package
- **Side** - Side view
- **Top** - Top view
- **Bottom** - Bottom view

#### Backend Features
- `ProductImage` model stores each image with metadata
- Automatic OCR text extraction from each image
- Image quality scoring (0-100%)
- Track who uploaded each image (user authorization)
- Separate endpoints for uploading and retrieving images by type

#### API Endpoints

```
POST /api/product-images/upload
- Upload multiple images for a product
- Requires: product_id, image files
- Authorization: JWT required

GET /api/product-images/<product_id>
- Get all images for a product
- Authorization: JWT required

GET /api/product-images/by-type/<product_id>/<image_type>
- Get specific image by type (front, back, side, top, bottom)
- Authorization: JWT required

DELETE /api/product-images/<image_id>
- Delete an image
- Authorization: Only uploader can delete
```

#### Frontend Components

**MultiAngleUploadForm.tsx**
- Drag-and-drop interface for 5 image angles
- Image preview before upload
- Batch upload all images at once
- Visual feedback for uploaded images

**ProductImageGallery.tsx**
- Grid view of all 5 image angles
- Image quality score display (color-coded)
- Click to expand and view full details
- Shows extracted OCR text
- Displays who uploaded and when

### 2. Comprehensive Review System

#### Review Features
- **Star Rating** (1-5 stars)
- **Compliance Feedback** (Compliant, Non-Compliant, Needs Improvement)
- **Issue Tracking** - List multiple issues found
- **Recommendations** - Suggest improvements
- **Department Tracking** - Track which department reviewed
- **Helpful/Unhelpful Voting** - Community feedback on reviews
- **Admin Approval** - Reviews require admin approval before display
- **User Authorization** - Users can only edit/delete their own reviews

#### ProductReview Model
```python
- id
- product_id (ForeignKey)
- user_id (ForeignKey)
- rating (1-5 stars)
- title
- review_text
- compliance_feedback (compliant, non_compliant, needs_improvement)
- issues_found (JSON array)
- recommendations
- department
- is_verified (verified inspection)
- helpful_count
- unhelpful_count
- status (pending, approved, rejected)
- created_at, updated_at
```

#### API Endpoints

```
POST /api/reviews/<product_id>
- Create a new review
- Requires: rating, title, review_text
- Authorization: JWT required

GET /api/reviews/<product_id>
- Get approved reviews for a product
- Supports pagination
- Returns average rating and review count
- Authorization: JWT required

PUT /api/reviews/<review_id>
- Update a review
- Authorization: Only reviewer can update

DELETE /api/reviews/<review_id>
- Delete a review
- Authorization: Only reviewer can delete

PUT /api/reviews/<review_id>/approve
- Approve a pending review
- Authorization: Admin only

PUT /api/reviews/<review_id>/reject
- Reject a pending review
- Authorization: Admin only

PUT /api/reviews/<review_id>/helpful
- Mark review as helpful
- Authorization: JWT required

PUT /api/reviews/<review_id>/unhelpful
- Mark review as unhelpful
- Authorization: JWT required

GET /api/reviews/user/<user_id>
- Get all reviews by a user
- Supports pagination

GET /api/reviews/compliance-summary/<product_id>
- Get compliance summary from all reviews
- Shows compliance percentage, common issues, recommendations
```

#### Frontend Components

**CreateReviewForm.tsx**
- Star rating input (interactive)
- Review title and text input
- Compliance feedback dropdown
- Issue tagging system (add/remove issues)
- Recommendations textarea
- Submit form with validation

**ReviewList.tsx**
- Display all approved reviews
- Show average star rating
- Display compliance status badge (color-coded)
- Helpful/Unhelpful voting buttons
- Pagination support
- Review metadata (reviewer name, department, date)

**ProductDetailPage.tsx**
- Tabbed interface (Images/Reviews)
- Product information display
- Multi-angle image upload and gallery
- Create review form
- Review list with pagination

### 3. User Authorization

#### Permission Model

```
Image Upload Permissions:
- User can upload images: Yes (JWT required)
- User can delete own images: Yes
- User can delete others' images: No (403 Forbidden)
- Admin can delete any image: Yes (with extended permissions)

Review Permissions:
- User can create review: Yes (JWT required)
- User can create only one review per product: Yes (enforced)
- User can edit own review: Yes
- User can delete own review: Yes
- Admin can approve reviews: Yes
- Admin can reject reviews: Yes
- Admin can view pending reviews: Yes
```

### 4. Database Schema Updates

#### ProductImage Table
```sql
CREATE TABLE product_images (
    id INTEGER PRIMARY KEY,
    product_id INTEGER FOREIGN KEY,
    image_type ENUM('front', 'back', 'side', 'top', 'bottom'),
    image_path VARCHAR(255),
    extracted_text TEXT,
    image_quality_score FLOAT,
    uploaded_by INTEGER FOREIGN KEY REFERENCES users(id),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

#### ProductReview Table
```sql
CREATE TABLE product_reviews (
    id INTEGER PRIMARY KEY,
    product_id INTEGER FOREIGN KEY,
    user_id INTEGER FOREIGN KEY,
    rating INTEGER (1-5),
    title VARCHAR(255),
    review_text TEXT,
    compliance_feedback VARCHAR(50),
    issues_found JSON,
    recommendations TEXT,
    department VARCHAR(100),
    is_verified BOOLEAN,
    helpful_count INTEGER,
    unhelpful_count INTEGER,
    status VARCHAR(50),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

## Usage Examples

### Upload Multiple Images

```typescript
const formData = new FormData();
formData.append('product_id', '123');
formData.append('front', frontImage);
formData.append('back', backImage);
formData.append('side', sideImage);
formData.append('top', topImage);
formData.append('bottom', bottomImage);

const result = await productService.uploadProductImages(formData);
```

### Create Review

```typescript
const review = await reviewService.createReview(productId, {
  rating: 4,
  title: 'Good product with minor issues',
  review_text: 'The product is generally compliant...',
  compliance_feedback: 'needs_improvement',
  issues_found: ['Font size too small', 'Missing manufacturer address'],
  recommendations: 'Increase font size and add full address',
});
```

### Get Reviews with Average Rating

```typescript
const result = await reviewService.getProductReviews(productId, page, perPage);
console.log(result.average_rating); // 4.5
console.log(result.review_count);   // 12
console.log(result.reviews);        // Array of reviews
```

## Quality Metrics

### Image Quality Score
- Based on OCR confidence
- Image brightness and contrast
- Text clarity and readability
- Scale: 0-100%
- Color-coded in UI: Green (80+), Yellow (60-80), Red (<60)

### Review Helpfulness
- Tracked via helpful/unhelpful votes
- Most helpful reviews ranked higher
- Community-driven feedback mechanism

## Security Considerations

1. **File Upload Security**
   - Validate file types (image/* only)
   - Check file size limits (50MB default)
   - Use secure filenames
   - Store outside web root

2. **Authorization**
   - JWT token validation on all endpoints
   - User-specific data isolation
   - Admin-only endpoints protected
   - Resource ownership verification

3. **Review Moderation**
   - Pending review status before display
   - Admin approval workflow
   - Ability to reject inappropriate reviews
   - Track reviewer identity

## Performance Optimization

1. **Image Processing**
   - Compress images before storage
   - Lazy load image galleries
   - Cache OCR results

2. **Reviews**
   - Paginate review lists (default 10 per page)
   - Cache average ratings
   - Index on product_id and status

3. **Frontend**
   - Lazy load review components
   - Debounce vote buttons
   - Cache user-specific reviews

## Future Enhancements

- [ ] Image comparison between angles
- [ ] Automated OCR text validation
- [ ] Review sentiment analysis
- [ ] Batch review export
- [ ] Review templates
- [ ] Reviewer reputation system
- [ ] Image annotation tools
- [ ] Mobile app image capture integration
- [ ] Real-time review notifications
- [ ] Review discussion threads
