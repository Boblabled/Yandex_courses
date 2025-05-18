#%% md
# Credits: this notebook belongs to [Practical DL](https://docs.google.com/forms/d/e/1FAIpQLScvrVtuwrHSlxWqHnLt1V-_7h2eON_mlRR6MUb3xEe5x9LuoA/viewform?usp=sf_link) course by Yandex School of Data Analysis.
#%%
import numpy as np
#%% md
# **Module** is an abstract class which defines fundamental methods necessary for a training a neural network. You do not need to change anything here, just read the comments.
#%%
class Module(object):
    """
    Basically, you can think of a module as of a something (black box) 
    which can process `input` data and produce `ouput` data.
    This is like applying a function which is called `forward`: 
        
        output = module.forward(input)
    
    The module should be able to perform a backward pass: to differentiate the `forward` function. 
    More, it should be able to differentiate it if is a part of chain (chain rule).
    The latter implies there is a gradient from previous step of a chain rule. 
    
        gradInput = module.backward(input, gradOutput)
    """
    def __init__ (self):
        self.output = None
        self.gradInput = None
        self.training = True
    
    def forward(self, input):
        """
        Takes an input object, and computes the corresponding output of the module.
        """
        return self.updateOutput(input)

    def backward(self,input, gradOutput):
        """
        Performs a backpropagation step through the module, with respect to the given input.
        
        This includes 
         - computing a gradient w.r.t. `input` (is needed for further backprop),
         - computing a gradient w.r.t. parameters (to update parameters while optimizing).
        """
        self.updateGradInput(input, gradOutput)
        self.accGradParameters(input, gradOutput)
        return self.gradInput
    

    def updateOutput(self, input):
        """
        Computes the output using the current parameter set of the class and input.
        This function returns the result which is stored in the `output` field.
        
        Make sure to both store the data in `output` field and return it. 
        """
        
        # The easiest case:
            
        # self.output = input 
        # return self.output
        
        pass

    def updateGradInput(self, input, gradOutput):
        """
        Computing the gradient of the module with respect to its own input. 
        This is returned in `gradInput`. Also, the `gradInput` state variable is updated accordingly.
        
        The shape of `gradInput` is always the same as the shape of `input`.
        
        Make sure to both store the gradients in `gradInput` field and return it.
        """
        
        # The easiest case:
        
        # self.gradInput = gradOutput 
        # return self.gradInput
        
        pass   
    
    def accGradParameters(self, input, gradOutput):
        """
        Computing the gradient of the module with respect to its own parameters.
        No need to override if module has no parameters (e.g. ReLU).
        """
        pass
    
    def zeroGradParameters(self): 
        """
        Zeroes `gradParams` variable if the module has params.
        """
        pass
        
    def getParameters(self):
        """
        Returns a list with its parameters. 
        If the module does not have parameters return empty list. 
        """
        return []
        
    def getGradParameters(self):
        """
        Returns a list with gradients with respect to its parameters. 
        If the module does not have parameters return empty list. 
        """
        return []
    
    def train(self):
        """
        Sets training mode for the module.
        Training and testing behaviour differs for Dropout, BatchNorm.
        """
        self.training = True
    
    def evaluate(self):
        """
        Sets evaluation mode for the module.
        Training and testing behaviour differs for Dropout, BatchNorm.
        """
        self.training = False
    
    def __repr__(self):
        """
        Pretty printing. Should be overrided in every module if you want 
        to have readable description. 
        """
        return "Module"
#%% md
# # Sequential container
#%% md
# **Define** a forward and backward pass procedures.
#%%
class Sequential(Module):
    """
         This class implements a container, which processes `input` data sequentially. 
         
         `input` is processed by each module (layer) in self.modules consecutively.
         The resulting array is called `output`. 
    """
    
    def __init__ (self):
        super(Sequential, self).__init__()
        self.modules = []
   
    def add(self, module):
        """
        Adds a module to the container.
        """
        self.modules.append(module)

    def updateOutput(self, input):
        """
        Basic workflow of FORWARD PASS:
        
            y_0    = module[0].forward(input)
            y_1    = module[1].forward(y_0)
            ...
            output = module[n-1].forward(y_{n-2})   
            
            
        Just write a little loop. 
        """

        # Your code goes here. ################################################
        out = input
        self.output = [out]
        for module in self.modules:
            out = module.forward(out)
            self.output.append(out)
        self.output = np.array(self.output)
        
        return self.output[-1]

    def backward(self, input, gradOutput):
        """
        Workflow of BACKWARD PASS:
            
            g_{n-1} = module[n-1].backward(y_{n-2}, gradOutput)
            g_{n-2} = module[n-2].backward(y_{n-3}, g_{n-1})
            ...
            g_1 = module[1].backward(y_0, g_2)   
            gradInput = module[0].backward(input, g_1)   
             
             
        !!!
                
        To ech module you need to provide the input, module saw while forward pass, 
        it is used while computing gradients. 
        Make sure that the input for `i-th` layer the output of `module[i]` (just the same input as in forward pass) 
        and NOT `input` to this Sequential module. 
        
        !!!
        
        """
        # Your code goes here. ################################################
        grad = gradOutput
        # print(self.modules)
        # print(len(self.modules), len(self.output))
        for i in reversed(range(len(self.modules))):
            # [input, y1, y2] [1 0]
            # y1 gradOutput
            # input g1
            grad = np.array(self.modules[i].backward(self.output[i], grad))
        self.gradInput = grad
            
        return self.gradInput
      

    def zeroGradParameters(self): 
        for module in self.modules:
            module.zeroGradParameters()
    
    def getParameters(self):
        """
        Should gather all parameters in a list.
        """
        return [x.getParameters() for x in self.modules]
    
    def getGradParameters(self):
        """
        Should gather all gradients w.r.t parameters in a list.
        """
        return [x.getGradParameters() for x in self.modules]
    
    def __repr__(self):
        string = "".join([str(x) + '\n' for x in self.modules])
        return string
    
    def __getitem__(self,x):
        return self.modules.__getitem__(x)
    
    def train(self):
        """
        Propagates training parameter through all modules
        """
        self.training = True
        for module in self.modules:
            module.train()
    
    def evaluate(self):
        """
        Propagates training parameter through all modules
        """
        self.training = False
        for module in self.modules:
            module.evaluate()
#%% md
# # Layers
#%% md
# ## 1. Linear transform layer
# Also known as dense layer, fully-connected layer, FC-layer, InnerProductLayer (in caffe), affine transform
# - input:   **`batch_size x n_feats1`**
# - output: **`batch_size x n_feats2`**
#%%
class Linear(Module):
    """
    A module which applies a linear transformation 
    A common name is fully-connected layer, InnerProductLayer in caffe. 
    
    The module should work with 2D input of shape (n_samples, n_feature).
    """
    def __init__(self, n_in, n_out):
        super(Linear, self).__init__()
       
        # This is a nice initialization
        stdv = 1./np.sqrt(n_in)
        self.W = np.random.uniform(-stdv, stdv, size = (n_out, n_in))
        self.b = np.random.uniform(-stdv, stdv, size = n_out)
        
        self.gradW = np.zeros_like(self.W)
        self.gradb = np.zeros_like(self.b)
        
    def updateOutput(self, input):
        # Your code goes here. ################################################
        self.output = np.dot(input, self.W.T) + self.b
        return self.output
    
    def updateGradInput(self, input, gradOutput):
        # Your code goes here. ################################################
        self.gradInput = np.dot(gradOutput, self.W)
        return self.gradInput
    
    def accGradParameters(self, input, gradOutput):
        # Your code goes here. ##################### ###########################
        # self.gradW += np.dot(gradOutput.T, input)
        # self.gradb += np.sum(gradOutput, axis=0)
        self.gradW = np.add(self.gradW, np.dot(gradOutput.T, input))
        self.gradb = np.add(self.gradb, np.sum(gradOutput, axis=0))
        pass
    
    def zeroGradParameters(self):
        self.gradW.fill(0)
        self.gradb.fill(0)
        
    def getParameters(self):
        return [self.W, self.b]
    
    def getGradParameters(self):
        return [self.gradW, self.gradb]
    
    def __repr__(self):
        s = self.W.shape
        q = 'Linear %d -> %d' %(s[1],s[0])
        return q
#%% md
# ## 2. SoftMax
# - input:   **`batch_size x n_feats`**
# - output: **`batch_size x n_feats`**
# 
# $\text{softmax}(x)_i = \frac{\exp x_i} {\sum_j \exp x_j}$
# 
# Recall that $\text{softmax}(x) == \text{softmax}(x - \text{const})$. It makes possible to avoid computing exp() from large argument.
#%%
class SoftMax(Module):
    def __init__(self):
         super(SoftMax, self).__init__()
    
    def updateOutput(self, input):
        # start with normalization for numerical stability
        self.output = np.subtract(input, input.max(axis=1, keepdims=True))
        # Your code goes here. ################################################
        self.output = np.exp(self.output)
        self.output = np.divide(self.output, np.sum(self.output, axis=-1, keepdims=True))
        return self.output
    
    def updateGradInput(self, input, gradOutput):
        # Your code goes here. ################################################
        self.gradInput = np.multiply(gradOutput, self.output)
        self.gradInput = np.sum(self.gradInput, axis=-1, keepdims=True)
        self.gradInput = np.subtract(gradOutput, self.gradInput)
        self.gradInput = np.multiply(self.output, self.gradInput)
        
        return self.gradInput
    
    def __repr__(self):
        return "SoftMax"
#%% md
# ## 3. LogSoftMax
# - input:   **`batch_size x n_feats`**
# - output: **`batch_size x n_feats`**
# 
# $\text{logsoftmax}(x)_i = \log\text{softmax}(x)_i = x_i - \log {\sum_j \exp x_j}$
# 
# The main goal of this layer is to be used in computation of log-likelihood loss.
#%%
class LogSoftMax(Module):
    def __init__(self):
         super(LogSoftMax, self).__init__()
    
    def updateOutput(self, input):
        # start with normalization for numerical stability
        self.output = np.subtract(input, input.max(axis=1, keepdims=True))
        
        # Your code goes here. ################################################
        self.output = np.subtract(self.output, np.log(np.sum(np.exp(self.output), axis=-1, keepdims=True)))
        return self.output
    
    def updateGradInput(self, input, gradOutput):
        # Your code goes here. ################################################
        softmax = np.subtract(input, input.max(axis=1, keepdims=True))
        softmax = np.exp(softmax)
        softmax = np.divide(softmax, np.sum(softmax, axis=-1, keepdims=True))
        
        self.gradInput = np.sum(gradOutput, axis=-1, keepdims=True)
        self.gradInput = np.multiply(softmax, self.gradInput)
        self.gradInput = np.subtract(gradOutput, self.gradInput)
        return self.gradInput
    
    def __repr__(self):
        return "LogSoftMax"
#%% md
# ## 4. Batch normalization
# One of the most significant recent ideas that impacted NNs a lot is [**Batch normalization**](http://arxiv.org/abs/1502.03167). The idea is simple, yet effective: the features should be whitened ($mean = 0$, $std = 1$) all the way through NN. This improves the convergence for deep models letting it train them for days but not weeks. **You are** to implement the first part of the layer: features normalization. The second part (`ChannelwiseScaling` layer) is implemented below.
# 
# - input:   **`batch_size x n_feats`**
# - output: **`batch_size x n_feats`**
# 
# The layer should work as follows. While training (`self.training == True`) it transforms input as $$y = \frac{x - \mu}  {\sqrt{\sigma + \epsilon}}$$
# where $\mu$ and $\sigma$ - mean and variance of feature values in **batch** and $\epsilon$ is just a small number for numericall stability. Also during training, layer should maintain exponential moving average values for mean and variance: 
# ```
#     self.moving_mean = self.moving_mean * alpha + batch_mean * (1 - alpha)
#     self.moving_variance = self.moving_variance * alpha + batch_variance * (1 - alpha)
# ```
# During testing (`self.training == False`) the layer normalizes input using moving_mean and moving_variance. 
# 
# Note that decomposition of batch normalization on normalization itself and channelwise scaling here is just a common **implementation** choice. In general "batch normalization" always assumes normalization + scaling.
#%%
class BatchNormalization(Module):
    EPS = 1e-3
    def __init__(self, alpha = 0.):
        super(BatchNormalization, self).__init__()
        self.alpha = alpha
        self.moving_mean = None 
        self.moving_variance = None
        
    def updateOutput(self, input):
        # Your code goes here. ################################################
        # use self.EPS please
     if self.moving_mean is None:
        self.moving_mean = np.zeros((1, input.shape[1]), dtype=input.dtype)
        self.moving_variance = np.ones((1, input.shape[1]), dtype=input.dtype)

     if self.training:
        batch_mean = np.mean(input, axis=0, keepdims=True)
        batch_var = np.var(input, axis=0, keepdims=True)
    
        self.moving_mean = self.alpha * self.moving_mean + (1 - self.alpha) * batch_mean
        self.moving_variance = self.alpha * self.moving_variance + (1 - self.alpha) * batch_var
    
     else:
        batch_mean = self.moving_mean
        batch_var = self.moving_variance
    
     self.input_centered = input - batch_mean
     self.std_inv = 1.0 / np.sqrt(batch_var + self.EPS)
            
     self.output = self.input_centered * self.std_inv
    
     return self.output
    
    def updateGradInput(self, input, gradOutput):
        var = np.mean((input - np.mean(input, axis=0, keepdims=True))**2, axis=0, keepdims=True)
        std = np.sqrt(var + self.EPS)

        x_hat = (input - np.mean(input, axis=0, keepdims=True)) / std

        dx_hat = gradOutput
        dmean = np.mean(dx_hat, axis=0, keepdims=True)
        dvar = np.mean(dx_hat * x_hat, axis=0, keepdims=True)
    
        self.gradInput = (1 / std) * (dx_hat - dmean - x_hat * dvar)
        
        return self.gradInput
    
    def __repr__(self):
        return "BatchNormalization"
#%%
class ChannelwiseScaling(Module):
    """
       Implements linear transform of input y = \gamma * x + \beta
       where \gamma, \beta - learnable vectors of length x.shape[-1]
    """
    def __init__(self, n_out):
        super(ChannelwiseScaling, self).__init__()

        stdv = 1./np.sqrt(n_out)
        self.gamma = np.random.uniform(-stdv, stdv, size=n_out)
        self.beta = np.random.uniform(-stdv, stdv, size=n_out)
        
        self.gradGamma = np.zeros_like(self.gamma)
        self.gradBeta = np.zeros_like(self.beta)

    def updateOutput(self, input):
        self.output = input * self.gamma + self.beta
        return self.output
        
    def updateGradInput(self, input, gradOutput):
        self.gradInput = gradOutput * self.gamma
        return self.gradInput
    
    def accGradParameters(self, input, gradOutput):
        self.gradBeta = np.sum(gradOutput, axis=0)
        self.gradGamma = np.sum(gradOutput*input, axis=0)
    
    def zeroGradParameters(self):
        self.gradGamma.fill(0)
        self.gradBeta.fill(0)
        
    def getParameters(self):
        return [self.gamma, self.beta]
    
    def getGradParameters(self):
        return [self.gradGamma, self.gradBeta]
    
    def __repr__(self):
        return "ChannelwiseScaling"
#%% md
# Practical notes. If BatchNormalization is placed after a linear transformation layer (including dense layer, convolutions, channelwise scaling) that implements function like `y = weight * x + bias`, than bias adding become useless and could be omitted since its effect will be discarded while batch mean subtraction. If BatchNormalization (followed by `ChannelwiseScaling`) is placed before a layer that propagates scale (including ReLU, LeakyReLU) followed by any linear transformation layer than parameter `gamma` in `ChannelwiseScaling` could be freezed since it could be absorbed into the linear transformation layer.
#%% md
# ## 5. Dropout
# Implement [**dropout**](https://www.cs.toronto.edu/~hinton/absps/JMLRdropout.pdf). The idea and implementation is really simple: just multimply the input by $Bernoulli(p)$ mask. Here $p$ is probability of an element to be zeroed.
# 
# This has proven to be an effective technique for regularization and preventing the co-adaptation of neurons.
# 
# While training (`self.training == True`) it should sample a mask on each iteration (for every batch), zero out elements and multiply elements by $1 / (1 - p)$. The latter is needed for keeping mean values of features close to mean values which will be in test mode. When testing this module should implement identity transform i.e. `self.output = input`.
# 
# - input:   **`batch_size x n_feats`**
# - output: **`batch_size x n_feats`**
#%%
class Dropout(Module):
    def __init__(self, p=0.5):
        super(Dropout, self).__init__()
        
        self.p = p
        self.mask = None
        
    def updateOutput(self, input):
        # Your code goes here. ################################################
        if self.training == False:
            self.output = input
        else:
            self.mask = np.random.random(input.shape) > self.p
            self.output = np.divide(np.multiply(input, self.mask), (1 - self.p))
        return  self.output
    
    def updateGradInput(self, input, gradOutput):
        # Your code goes here. ################################################
        if self.training == False:
            self.gradInput = gradOutput
        else:
            self.gradInput = np.divide(np.multiply(gradOutput, self.mask), (1 - self.p))
        return self.gradInput
        
    def __repr__(self):
        return "Dropout"
#%% md
# # Activation functions
#%% md
# Here's the complete example for the **Rectified Linear Unit** non-linearity (aka **ReLU**): 
#%%
class ReLU(Module):
    def __init__(self):
         super(ReLU, self).__init__()
    
    def updateOutput(self, input):
        self.output = np.maximum(input, 0)
        return self.output
    
    def updateGradInput(self, input, gradOutput):
        self.gradInput = np.multiply(gradOutput, input > 0)
        return self.gradInput
    
    def __repr__(self):
        return "ReLU"
#%% md
# ## 6. Leaky ReLU
# Implement [**Leaky Rectified Linear Unit**](http://en.wikipedia.org/wiki%2FRectifier_%28neural_networks%29%23Leaky_ReLUs). Expriment with slope. 
#%%
class LeakyReLU(Module):
    def __init__(self, slope = 0.03):
        super(LeakyReLU, self).__init__()
            
        self.slope = slope
        
    def updateOutput(self, input):
        # Your code goes here. ################################################
        self.output = np.maximum(input, np.multiply(input, self.slope))
        return  self.output
    
    def updateGradInput(self, input, gradOutput):
        # Your code goes here. ################################################
        self.gradInput = np.where(input > 0, gradOutput,  np.multiply(gradOutput, self.slope))
        return self.gradInput
    
    def __repr__(self):
        return "LeakyReLU"
#%% md
# ## 7. ELU
# Implement [**Exponential Linear Units**](http://arxiv.org/abs/1511.07289) activations.
#%%
class ELU(Module):
    def __init__(self, alpha = 1.0):
        super(ELU, self).__init__()
        
        self.alpha = alpha
        
    def updateOutput(self, input):
        # Your code goes here. ################################################
        self.output = np.where(input > 0, input, np.multiply(np.subtract(np.exp(input), 1), self.alpha))
        return self.output
    
    def updateGradInput(self, input, gradOutput):
        # Your code goes here. ################################################
        self.gradInput =  np.multiply(gradOutput, np.where(input > 0, 1,  np.multiply(np.exp(input), self.alpha)))
        return self.gradInput
    
    def __repr__(self):
        return "ELU"
#%% md
# ## 8. SoftPlus
# Implement [**SoftPlus**](https://en.wikipedia.org/wiki%2FRectifier_%28neural_networks%29) activations. Look, how they look a lot like ReLU.
#%%
class SoftPlus(Module):
    def __init__(self):
        super(SoftPlus, self).__init__()
    
    def updateOutput(self, input):
        # Your code goes here. ################################################
        self.output = np.log(np.add(1, np.exp(input)))
        return  self.output
    
    def updateGradInput(self, input, gradOutput):
        # Your code goes here. ################################################
        self.gradInput = np.multiply(gradOutput, np.divide(np.exp(input), np.add(1, np.exp(input))))
        return self.gradInput
    
    def __repr__(self):
        return "SoftPlus"
#%% md
# # Criterions
#%% md
# Criterions are used to score the models answers. 
#%%
class Criterion(object):
    def __init__ (self):
        self.output = None
        self.gradInput = None
        
    def forward(self, input, target):
        """
            Given an input and a target, compute the loss function 
            associated to the criterion and return the result.
            
            For consistency this function should not be overrided,
            all the code goes in `updateOutput`.
        """
        return self.updateOutput(input, target)

    def backward(self, input, target):
        """
            Given an input and a target, compute the gradients of the loss function
            associated to the criterion and return the result. 

            For consistency this function should not be overrided,
            all the code goes in `updateGradInput`.
        """
        return self.updateGradInput(input, target)
    
    def updateOutput(self, input, target):
        """
        Function to override.
        """
        return self.output

    def updateGradInput(self, input, target):
        """
        Function to override.
        """
        return self.gradInput   

    def __repr__(self):
        """
        Pretty printing. Should be overrided in every module if you want 
        to have readable description. 
        """
        return "Criterion"
#%% md
# The **MSECriterion**, which is basic L2 norm usually used for regression, is implemented here for you.
# - input:   **`batch_size x n_feats`**
# - target: **`batch_size x n_feats`**
# - output: **scalar**
#%%
class MSECriterion(Criterion):
    def __init__(self):
        super(MSECriterion, self).__init__()
        
    def updateOutput(self, input, target):   
        self.output = np.sum(np.power(input - target,2)) / input.shape[0]
        return self.output 
 
    def updateGradInput(self, input, target):
        self.gradInput  = (input - target) * 2 / input.shape[0]
        return self.gradInput

    def __repr__(self):
        return "MSECriterion"
#%% md
# ## 9. Negative LogLikelihood criterion (numerically unstable)
# You task is to implement the **ClassNLLCriterion**. It should implement [multiclass log loss](http://scikit-learn.org/stable/modules/model_evaluation.html#log-loss). Nevertheless there is a sum over `y` (target) in that formula, 
# remember that targets are one-hot encoded. This fact simplifies the computations a lot. Note, that criterions are the only places, where you divide by batch size. Also there is a small hack with adding small number to probabilities to avoid computing log(0).
# - input:   **`batch_size x n_feats`** - probabilities
# - target: **`batch_size x n_feats`** - one-hot representation of ground truth
# - output: **scalar**
# 
# 
#%%
class ClassNLLCriterionUnstable(Criterion):
    EPS = 1e-15
    def __init__(self):
        a = super(ClassNLLCriterionUnstable, self)
        super(ClassNLLCriterionUnstable, self).__init__()
        
    def updateOutput(self, input, target): 
        
        # Use this trick to avoid numerical errors
        input_clamp = np.clip(input, self.EPS, 1 - self.EPS)
        
        # Your code goes here. ################################################
        self.output = np.mean(-np.sum(np.multiply(target, np.log(input_clamp)), axis=1, keepdims=True))
        return self.output

    def updateGradInput(self, input, target):
        
        # Use this trick to avoid numerical errors
        input_clamp = np.clip(input, self.EPS, 1 - self.EPS)
                
        # Your code goes here. ################################################
        batch_size = input.shape[0]
        self.gradInput = np.divide(-target, (np.multiply(input_clamp, batch_size)))
        return self.gradInput
    
    def __repr__(self):
        return "ClassNLLCriterionUnstable"
#%% md
# ## 10. Negative LogLikelihood criterion (numerically stable)
# - input:   **`batch_size x n_feats`** - log probabilities
# - target: **`batch_size x n_feats`** - one-hot representation of ground truth
# - output: **scalar**
# 
# Task is similar to the previous one, but now the criterion input is the output of log-softmax layer. This decomposition allows us to avoid problems with computation of forward and backward of log().
#%%
class ClassNLLCriterion(Criterion):
    def __init__(self):
        a = super(ClassNLLCriterion, self)
        super(ClassNLLCriterion, self).__init__()
        
    def updateOutput(self, input, target): 
        # Your code goes here. ################################################
        self.output = np.mean(-np.sum(np.multiply(target, input), axis=1))
        return self.output

    def updateGradInput(self, input, target):
        # Your code goes here. ################################################
        batch_size = input.shape[0]
        self.gradInput = np.divide(-target, batch_size)
        return self.gradInput
    
    def __repr__(self):
        return "ClassNLLCriterion"
#%% md
# # Optimizers
#%% md
# ### SGD optimizer with momentum
# - `variables` - list of lists of variables (one list per layer)
# - `gradients` - list of lists of current gradients (same structure as for `variables`, one array for each var)
# - `config` - dict with optimization parameters (`learning_rate` and `momentum`)
# - `state` - dict with optimizator state (used to save accumulated gradients)
#%%
def sgd_momentum(variables, gradients, config, state):  
    # 'variables' and 'gradients' have complex structure, accumulated_grads will be stored in a simpler one
    state.setdefault('accumulated_grads', {})
    
    var_index = 0 
    for current_layer_vars, current_layer_grads in zip(variables, gradients): 
        for current_var, current_grad in zip(current_layer_vars, current_layer_grads):
            
            old_grad = state['accumulated_grads'].setdefault(var_index, np.zeros_like(current_grad))
            
            np.add(config['momentum'] * old_grad, config['learning_rate'] * current_grad, out=old_grad)
            
            current_var -= old_grad
            var_index += 1     
#%% md
# ## 11. [Adam](https://arxiv.org/pdf/1412.6980.pdf) optimizer
# - `variables` - list of lists of variables (one list per layer)
# - `gradients` - list of lists of current gradients (same structure as for `variables`, one array for each var)
# - `config` - dict with optimization parameters (`learning_rate`, `beta1`, `beta2`, `epsilon`)
# - `state` - dict with optimizator state (used to save 1st and 2nd moment for vars)
# 
# Formulas for optimizer:
# 
# Current step learning rate: $$\text{lr}_t = \text{learning\_rate} * \frac{\sqrt{1-\beta_2^t}}{1-\beta_1^t}$$
# First moment of var: $$\mu_t = \beta_1 * \mu_{t-1} + (1 - \beta_1)*g$$ 
# Second moment of var: $$v_t = \beta_2 * v_{t-1} + (1 - \beta_2)*g*g$$
# New values of var: $$\text{variable} = \text{variable} - \text{lr}_t * \frac{m_t}{\sqrt{v_t} + \epsilon}$$
#%%
def adam_optimizer(variables, gradients, config, state):  
    # 'variables' and 'gradients' have complex structure, accumulated_grads will be stored in a simpler one
    state.setdefault('m', {})  # first moment vars
    state.setdefault('v', {})  # second moment vars
    state.setdefault('t', 0)   # timestamp
    state['t'] += 1
    for k in ['learning_rate', 'beta1', 'beta2', 'epsilon']:
        assert k in config, config.keys()
    
    var_index = 0 
    lr_t = config['learning_rate'] * np.sqrt(1 - config['beta2']**state['t']) / (1 - config['beta1']**state['t'])
    for current_layer_vars, current_layer_grads in zip(variables, gradients): 
        for current_var, current_grad in zip(current_layer_vars, current_layer_grads):
            var_first_moment = state['m'].setdefault(var_index, np.zeros_like(current_grad))
            var_second_moment = state['v'].setdefault(var_index, np.zeros_like(current_grad))
            
            # <YOUR CODE> #######################################
            # update `current_var_first_moment`, `var_second_moment` and `current_var` values
            #np.add(... , out=var_first_moment)
            #np.add(... , out=var_second_moment)
            #current_var -= ...
            np.add(config['beta1'] * var_first_moment, (1 - config['beta1']) * current_grad, out=var_first_moment)
            np.add(config['beta2'] * var_second_moment, (1 - config['beta2']) * (current_grad ** 2), out=var_second_moment)

            current_var -= lr_t * var_first_moment / (np.sqrt(var_second_moment) + config['epsilon'])
            
            # small checks that you've updated the state; use np.add for rewriting np.arrays values
            assert var_first_moment is state['m'].get(var_index)
            assert var_second_moment is state['v'].get(var_index)
            var_index += 1

#%% md
# # Layers for advanced track homework
# You **don't need** to implement it if you are working on `homework_main-basic.ipynb`
#%% md
# ## 12. Conv2d [Advanced]
# - input:   **`batch_size x in_channels x h x w`**
# - output: **`batch_size x out_channels x h x w`**
# 
# You should implement something like pytorch `Conv2d` layer with `stride=1` and zero-padding outside of image using `scipy.signal.correlate` function.
# 
# Practical notes:
# - While the layer name is "convolution", the most of neural network frameworks (including tensorflow and pytorch) implement operation that is called [correlation](https://en.wikipedia.org/wiki/Cross-correlation#Cross-correlation_of_deterministic_signals) in signal processing theory. So **don't use** `scipy.signal.convolve` since it implements [convolution](https://en.wikipedia.org/wiki/Convolution#Discrete_convolution) in terms of signal processing.
# - It's rather ok to implement convolution over 4d array using 2 nested loops: one over batch size dimension and another one over output filters dimension
# - Having troubles with understanding how to implement the layer? 
#  - Check the last year video of lecture 3 (starting from ~1:14:20)
#  - May the google be with you
#%%
import scipy as sp
import scipy.signal

class Conv2d(Module):
    def __init__(self, in_channels, out_channels, kernel_size):
        super(Conv2d, self).__init__()
        assert kernel_size % 2 == 1, kernel_size
       
        stdv = 1./np.sqrt(in_channels)
        self.W = np.random.uniform(-stdv, stdv, size = (out_channels, in_channels, kernel_size, kernel_size))
        self.b = np.random.uniform(-stdv, stdv, size = (out_channels,))
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        
        self.gradW = np.zeros_like(self.W)
        self.gradb = np.zeros_like(self.b)
        
    def updateOutput(self, input):
        pad_size = self.kernel_size // 2
        # YOUR CODE ##############################
        # 1. zero-pad the input array
        # 2. compute convolution using scipy.signal.correlate(... , mode='valid')
        # 3. add bias value
        
        padded = np.pad(input, pad_width=((0,0), (0,0), (pad_size,pad_size), (pad_size,pad_size)), mode='constant')
        batch_size, _, W, H = input.shape
        self.output = np.zeros((batch_size, self.out_channels, W, H))
        for batch in range(batch_size):
            for out_channel in range(self.out_channels):
                self.output[batch, out_channel] = np.sum(scipy.signal.correlate(padded[batch], self.W[out_channel], mode='valid'), axis=0) + self.b[out_channel]
                        
        return self.output
    
    def updateGradInput(self, input, gradOutput):
        pad_size = self.kernel_size // 2
        # YOUR CODE ##############################
        # 1. zero-pad the gradOutput
        # 2. compute 'self.gradInput' value using scipy.signal.correlate(... , mode='valid')
        
        padded_grad = np.pad(gradOutput,pad_width=((0,0), (0,0), (pad_size,pad_size), (pad_size,pad_size)),mode='constant')
        
        self.gradInput = np.zeros_like(input)
        
        rotated_W = np.rot90(self.W, 2, axes=(2,3))
        for batch in range(input.shape[0]):
            for in_channel in range(self.in_channels):
                for out_channel in range(self.out_channels): 
                    self.gradInput[batch, in_channel] += scipy.signal.correlate(padded_grad[batch, out_channel], rotated_W[out_channel, in_channel], mode='valid')
        
        return self.gradInput
    
    def accGradParameters(self, input, gradOutput):
        pad_size = self.kernel_size // 2
        # YOUR CODE #############
        # 1. zero-pad the input
        # 2. compute 'self.gradW' using scipy.signal.correlate(... , mode='valid')
        # 3. compute 'self.gradb' - formulas like in Linear of ChannelwiseScaling layers
        
        padded = np.pad(input, pad_width=((0,0), (0,0), (pad_size,pad_size), (pad_size,pad_size)), mode='constant')
    
        self.gradW = np.zeros_like(self.W)
        for batch in range(input.shape[0]): 
            for out_channel in range(self.out_channels):
                for in_channel in range(self.in_channels):
                    self.gradW[out_channel, in_channel] += scipy.signal.correlate(padded[batch, in_channel], gradOutput[batch, out_channel], mode='valid')
        
        self.gradb = np.sum(gradOutput, axis=(0,2,3))
    
    
    def zeroGradParameters(self):
        self.gradW.fill(0)
        self.gradb.fill(0)
        
    def getParameters(self):
        return [self.W, self.b]
    
    def getGradParameters(self):
        return [self.gradW, self.gradb]
    
    def __repr__(self):
        s = self.W.shape
        q = 'Conv2d %d -> %d' %(s[1],s[0])
        return q
#%% md
# ## 13. MaxPool2d [Advanced]
# - input:   **`batch_size x n_input_channels x h x w`**
# - output: **`batch_size x n_output_channels x h // kern_size x w // kern_size`**
# 
# You are to implement simplified version of pytorch `MaxPool2d` layer with stride = kernel_size. Please note, that it's not a common case that stride = kernel_size: in AlexNet and ResNet kernel_size for max-pooling was set to 3, while stride was set to 2. We introduce this restriction to make implementation simplier.
# 
# Practical notes:
# - During forward pass what you need to do is just to reshape the input tensor to `[n, c, h / kern_size, kern_size, w / kern_size, kern_size]`, swap two axes and take maximums over the last two dimensions. Reshape + axes swap is sometimes called space-to-batch transform.
# - During backward pass you need to place the gradients in positions of maximal values taken during the forward pass
# - In real frameworks the indices of maximums are stored in memory during the forward pass. It is cheaper than to keep the layer input in memory and recompute the maximums.
#%%
class MaxPool2d(Module):
    def __init__(self, kernel_size):
        super(MaxPool2d, self).__init__()
        self.kernel_size = kernel_size
        self.gradInput = None
                    
    def updateOutput(self, input):
        input_h, input_w = input.shape[-2:]
        # your may remove these asserts and implement MaxPool2d with padding
        assert input_h % self.kernel_size == 0  
        assert input_w % self.kernel_size == 0
        
        # YOUR CODE #############################
        batch_size, channels = input.shape[:2]
        self.output = np.swapaxes(input.copy().reshape(batch_size, channels, input_h // self.kernel_size, self.kernel_size, input_w // self.kernel_size, self.kernel_size), 3, 4)
        self.output = self.output.reshape(batch_size, channels, input_h // self.kernel_size, input_w // self.kernel_size, self.kernel_size**2)
        
        self.max_indices = np.argmax(self.output, axis=-1)
        self.output = np.max(self.output, axis=-1)

        return self.output
    
    def updateGradInput(self, input, gradOutput):
        # YOUR CODE #############################
        batch_size, channels, input_h, input_w = input.shape
    
        self.gradInput = np.zeros_like(input)
        
        for batch in range(batch_size):
            for channel in range(channels):
                for i in range(input_h // self.kernel_size):
                    for j in range(input_w // self.kernel_size):
                        max_idx = self.max_indices[batch, channel, i, j]
                        self.gradInput[batch, channel, 
                                       i * self.kernel_size + max_idx // self.kernel_size, 
                                       j * self.kernel_size + max_idx % self.kernel_size] = gradOutput[batch, channel, i, j]
        
        return self.gradInput
    
    def __repr__(self):
        q = 'MaxPool2d, kern %d, stride %d' %(self.kernel_size, self.kernel_size)
        return q
#%% md
# ### Flatten layer
# Just reshapes inputs and gradients. It's usually used as proxy layer between Conv2d and Linear.
#%%
class Flatten(Module):
    def __init__(self):
         super(Flatten, self).__init__()
    
    def updateOutput(self, input):
        self.output = input.reshape(len(input), -1)
        return self.output
    
    def updateGradInput(self, input, gradOutput):
        self.gradInput = gradOutput.reshape(input.shape)
        return self.gradInput
    
    def __repr__(self):
        return "Flatten"
#%%
