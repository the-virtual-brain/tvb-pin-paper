class ICAAdapter(ABCAsynchronous):
    
    _ui_name = "Independent Component Analysis"
    _ui_description = "ICA for a TimeSeries input DataType."
    _ui_subsection = "ica"
    
    
    def get_input_tree(self):
        algorithm = fastICA()
        algorithm.trait.bound = self.INTERFACE_ATTRIBUTES_ONLY
        tree = algorithm.interface[self.INTERFACE_ATTRIBUTES]
        filt = FilterChain(fields=
                [FilterChain.datatype + '._nr_dimensions'],
                operations=["=="], values=[4])
        for node in tree:
            if node['name'] == 'time_series':
                node['conditions'] = filt
        return tree
    
    
    def get_output(self):
        return [IndependentComponents]
    
    def configure(self, time_series, n_components=None):
        self.input_shape = time_series.read_data_shape()
        log_debug_array(LOG, time_series, "time_series")
        
        self.algorithm = fastICA()
        self.algorithm.n_components = \
                n_components or self.input_shape[2]
        
    def get_required_memory_size(self, **kwargs):
        used_shape = (self.input_shape[0], 1, 
                self.input_shape[2], self.input_shape[3])
        input_size = numpy.prod(used_shape) * 8.0
        output_size = self.algorithm.\
                            result_size(used_shape)
        return input_size + output_size  
    
    def launch(self, time_series, n_components=None):
        ica_result = IndependentComponents(
            source=time_series,
            n_components=int(self.algorithm.n_components),
            storage_path=self.storage_path)
        
        # 4-D simulation time series
        node_slice = [slice(self.input_shape[0]), 
                None, slice(self.input_shape[2]), 
                slice(self.input_shape[3])]
        
        ts = TimeSeries(use_storage=False)
        for var in range(self.input_shape[1]):
            node_slice[1] = slice(var, var + 1)
            ts.data = time_series.read_data_slice(
                    tuple(node_slice))
            self.algorithm.time_series = ts 
            partial_ica = self.algorithm.evaluate()
            ica_result.write_data_slice(partial_ica)
        ica_result.close_file()
        return ica_result
