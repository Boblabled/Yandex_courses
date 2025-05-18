import numpy as np
def compute_sobel_gradients_two_loops(image):
    # Get image dimensions
    height, width = image.shape

    # Initialize output gradients
    gradient_x = np.zeros_like(image, dtype=np.float64)
    gradient_y = np.zeros_like(image, dtype=np.float64)

    # Pad the image with zeros to handle borders
    padded_image = np.pad(image, ((1, 1), (1, 1)), mode='constant', constant_values=0)
# __________end of block__________

    # Define the Sobel kernels for X and Y gradients
    sobel_x = np.array([[-1., 0., 1.],
                        [-2., 0., 2.],
                        [-1., 0., 1.]]) # YOUR CODE HERE
    sobel_y = np.array([[-1., -2., -1.],
                        [0., 0., 0.],
                        [1., 2., 1.]]) # YOUR CODE HERE

    # Apply Sobel filter for X and Y gradients using convolution
    for i in range(1, height + 1):
        for j in range(1, width + 1):
            # YOUR CODE HERE
            gradient_x[j-1, i-1] = np.sum(np.multiply(padded_image[j-1:j+2, i-1:i+2].copy(), sobel_x))
            gradient_y[j-1, i-1] = np.sum(np.multiply(padded_image[j-1:j+2, i-1:i+2].copy(), sobel_y))
    return gradient_x, gradient_y


def compute_gradient_magnitude(sobel_x, sobel_y):
    '''
    Compute the magnitude of the gradient given the x and y gradients.

    Inputs:
        sobel_x: numpy array of the x gradient.
        sobel_y: numpy array of the y gradient.

    Returns:
        magnitude: numpy array of the same shape as the input [0] with the magnitude of the gradient.
    '''
    # YOUR CODE HERE
    return np.sqrt(np.square(sobel_x.copy()) + np.square(sobel_y.copy()))


def compute_gradient_direction(sobel_x, sobel_y):
    '''
    Compute the direction of the gradient given the x and y gradients. Angle must be in degrees in the range (-180; 180].
    Use arctan2 function to compute the angle.

    Inputs:
        sobel_x: numpy array of the x gradient.
        sobel_y: numpy array of the y gradient.

    Returns:
        gradient_direction: numpy array of the same shape as the input [0] with the direction of the gradient.
    '''
    # YOUR CODE HERE
    return np.degrees(np.arctan2(sobel_y, sobel_x))


cell_size = 7


def compute_hog(image, pixels_per_cell=(cell_size, cell_size), bins=9):
    # 1. Convert the image to grayscale if it's not already (assuming the image is in RGB or BGR)
    if len(image.shape) == 3:
        image = np.mean(image, axis=2)  # Simple averaging to convert to grayscale

    # 2. Compute gradients with Sobel filter
    gradient_x, gradient_y = compute_sobel_gradients_two_loops(image)  # YOUR CODE HERE

    # 3. Compute gradient magnitude and direction
    magnitude = compute_gradient_magnitude(gradient_x, gradient_y)  # YOUR CODE HERE
    direction = compute_gradient_direction(gradient_x, gradient_y)  # YOUR CODE HERE

    # 4. Create histograms of gradient directions for each cell
    cell_height, cell_width = pixels_per_cell
    n_cells_x = image.shape[1] // cell_width
    n_cells_y = image.shape[0] // cell_height

    histograms = np.zeros((n_cells_y, n_cells_x, bins))

    bin_size = 360 / bins

    for i in range(n_cells_y):
        for j in range(n_cells_x):
            cell_magnitude = magnitude[i * cell_height:i * cell_height + cell_height,
                             j * cell_width:j * cell_width + cell_width].flatten()
            cell_direction = direction[i * cell_height:i * cell_height + cell_height,
                             j * cell_width:j * cell_width + cell_width].flatten()
            cell_direction = cell_direction + 180
            histogram = np.zeros(bins)

            for k in range(cell_direction.size):

                angle = cell_direction[k]
                mag = cell_magnitude[k]

                bin_ = int(angle // bin_size) % bins
                if angle % bin_size == 0:
                    bin_ -= 1
                histogram[bin_] += mag

            hist_sum = np.sum(histogram)
            if hist_sum != 0:
                histograms[i, j, :] = histogram / hist_sum

    return histograms
