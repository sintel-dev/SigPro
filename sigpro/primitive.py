from sigpro.contributing import _get_primitive_args, _get_primitive_spec, _check_primitive_type_and_subtype
import json
import inspect
import copy
from mlblocks.discovery import load_primitive
from mlblocks.mlblock import import_object, MLBlock


class Primitive(): 

    def __init__(self, primitive, primitive_type, primitive_subtype, 
                primitive_function = None, init_params = {}):

        """
        Initialize primitive object. 
        """
        self.primitive = primitive
        self.tag = primitive.split('.')[-1]
        self.primitive_type = primitive_type
        self.primitive_subtype = primitive_subtype
        self.tunable_hyperparameters = {}
        self.fixed_hyperparameters = {}
        self.context_arguments = []
        primitive_spec = _get_primitive_spec(primitive_type, primitive_subtype)
        self.primitive_inputs = primitive_spec['args']
        self.primitive_outputs = primitive_spec['output']

        _check_primitive_type_and_subtype(primitive_type, primitive_subtype)

        if primitive_function == None:
            primitive_function = import_object(primitive)
        self.primitive_function = primitive_function
        self.hyperparameter_values = init_params 

    def get_name(self):
        return self.primitive
    def get_tag(self):
        return self.tag
    def get_inputs(self):
        return copy.deepcopy(self.primitive_inputs)
    def get_outputs(self):
        return copy.deepcopy(self.primitive_outputs)

    def get_type_subtype(self):
        return self.primitive_type, self.primitive_subtype

    def _validate_primitive_spec(self): #check compatibility of given parameters.
        
        primitive_args = _get_primitive_args(
            self.primitive_function,
            self.primitive_inputs,
            self.context_arguments,
            self.fixed_hyperparameters,
            self.tunable_hyperparameters
        )
    
    
    def get_hyperparam_dict(self, name = None):
        """
        Return the dictionary of parameters (for use in larger pipelines such as Linear, etc)
        """
        if name == None:
            name = self.tag
        return { 'name': name, 'primitive': self.primitive, 'init_params': self.hyperparameter_values}


    def set_tag(self, tag):
        self.tag = tag
        return self
    def set_primitive_function(self, primitive_function):
        self.primitive_function = primitive_function

    def set_primitive_inputs(self, primitive_inputs): 
        self.primitive_inputs = primitive_inputs
            
    def set_primitive_outputs(self, primitive_outputs): 
        self.primitive_outputs = primitive_outputs

    def _set_primitive_type(self, primitive_type):
        self.primitive_type = primitive_type
    def _set_primitive_subtype(self, primitive_subtype):
        self.primitive_subtype = primitive_subtype

    def set_context_arguments(self, context_arguments):
        self.context_arguments = context_arguments

    def set_tunable_hyperparameters(self, tunable_hyperparameters):
        self.tunable_hyperparameters = tunable_hyperparameters

    def set_fixed_hyperparameters(self, fixed_hyperparameters):
        self.fixed_hyperparameters = fixed_hyperparameters

    def add_context_arguments(self, context_arguments):
        for arg in context_argments:
            if arg not in self.context_arguments:
                context_arguments.append(arg)
    def add_fixed_hyperparameter(self, hyperparams):
        for hyperparam in hyperparams:
            self.fixed_hyperparameters[hyperparam] = hyperparams[hyperparam]
    def add_tunable_hyperparameter(self, hyperparams):
        for hyperparam in hyperparams:
            self.tunable_hyperparameters[hyperparam] = hyperparams[hyperparam]
    def remove_context_arguments(self, context_arguments):
        for arg in context_argments:
            if arg in self.context_arguments:
                context_arguments.remove(arg)
    def remove_fixed_hyperparameter(self, hyperparams):
        for hyperparam in hyperparams:
            del self.fixed_hyperparameters[hyperparam]
    def remove_tunable_hyperparameter(self, hyperparams):
        for hyperparam in hyperparams:
            del self.tunable_hyperparameters[hyperparam]



class TransformationPrimitive(Primitive):

    def __init__(self, primitive, primitive_subtype,  init_params = {}):
        super().__init__(primitive, 'transformation',primitive_subtype, init_params = init_params)

    pass

class AmplitudeTransformation(TransformationPrimitive):

    def __init__(self, primitive, init_params = {}):
        super().__init__(primitive, 'amplitude', init_params = init_params)

    pass


class FrequencyTransformation(TransformationPrimitive):

    def __init__(self, primitive, init_params = {}):
        super().__init__(primitive,  'frequency', init_params = init_params)

    pass

class FrequencyTimeTransformation(TransformationPrimitive):

    def __init__(self, primitive, init_params = {}):
        super().__init__(primitive, 'frequency_time', init_params = init_params)




class ComparativeTransformation(TransformationPrimitive):
    pass


class AggregationPrimitive(Primitive):
    def __init__(self, primitive, primitive_subtype, init_params = {}):
        super().__init__(primitive, 'aggregation', primitive_subtype, init_params = init_params)


class AmplitudeAggregation(AggregationPrimitive):

    def __init__(self, primitive,  init_params = {}):
        super().__init__(primitive, 'amplitude', init_params = init_params)

class FrequencyAggregation(AggregationPrimitive):

    def __init__(self, primitive,  init_params = {}):
        super().__init__(primitive,  'frequency',  init_params = init_params)

class FrequencyTimeAggregation(AggregationPrimitive):

    def __init__(self, primitive, init_params = {}):
        super().__init__(primitive, 'frequency_time', init_params = init_params)


class ComparativeAggregation(AggregationPrimitive):
    pass