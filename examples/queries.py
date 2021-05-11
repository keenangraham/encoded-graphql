from schema import schema


print(
    schema.execute(
        '''
            {
                 encoded(at_id: "/experiments/ENCSR688AWP/") { at_id }
            }
        '''
    )
)


print(
    schema.execute(
        '''
            {
                 encoded(at_id: "/experiments/ENCSR688AWP/") {
                    embedded {
                        ... on Experiment {
                            status
                            uuid
                            at_id
                            files {
                                at_id 
                                embedded {
                                    ... on File {
                                        status
                                        award {
                                            at_id
                                        }
                                        quality_metrics {
                                            at_id
                                            embedded {
                                                ... on SamtoolsStatsQualityMetric {
                                                    at_id
                                                    status
                                                    step_run { at_id } 
                                                    reads_mapped
                                                    reads_paired
                                                    maximum_length
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                 }
            }
        '''
    )
)


print(
    schema.execute(
        '''
            {
                 file1: file_(at_id: "/files/ENCFF566IYJ/") { status uuid }
            }
        '''
    )
)


print(
    schema.execute(
        '''
            {
                 file1: file_(at_id: "/files/ENCFF566IYJ/")
                      {
                           status
                           uuid
                           technical_replicates
                           at_id
                           at_type
                           controlled_by { at_id } 
                      }
                 file2: file_(at_id: "/files/ENCFF681NFS/")
                      {
                           status
                           uuid
                           controlled_by {
                               at_id
                               embedded { ...on File { at_id status }}
                           }
                           at_id
                           at_type
                       }
            }
    '''
))
