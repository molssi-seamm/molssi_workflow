# -*- coding: utf-8 -*-
"""The ExecWorkflow object does what it name implies: it executes, or
runs, a given flowchart.

It provides the environment for running the computational tasks
locally or remotely, using what is commonly called workflow management
system (WMS).  The WMS concept, as used here, means tools that run
given tasks without knowing anything about chemistry. The chemistry
specialization is contained in the Flowchart and the nodes that it
contains."""

import logging
import seamm
import seamm_util.printing as printing
from seamm_util.printing import FormattedText as __

logger = logging.getLogger(__name__)
job = printing.getPrinter()


class ExecFlowchart(object):
    def __init__(self, flowchart=None):
        """Execute a flowchart, providing support for the actual
        execution of codes """

        self.flowchart = flowchart

    def run(self, root=None):
        if not self.flowchart:
            raise RuntimeError('There is no flowchart to run!')

        logger.debug('Creating global variables space')
        seamm.flowchart_variables = seamm.Variables()
        
        self.flowchart.root_directory = root

        # Correctly number the nodes
        self.flowchart.set_ids()

        # Write out an initial summary of the flowchart before doing anything
        # Reset the visited flag for traversal
        self.flowchart.reset_visited()

        # Get the start node
        next_node = self.flowchart.get_node('1')

        # describe ourselves
        job.job(('\nDescription of the flowchart'
                 '\n----------------------------'))

        while next_node:
            next_node = next_node.describe()
        job.job('')

        # And actually run it!
        job.job(('Running the flowchart\n'
                 '---------------------'))

        next_node = self.flowchart.get_node('1')
        while next_node:
            next_node = next_node.run()