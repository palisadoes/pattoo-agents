#!/usr/bin/env python3
"""Pattoo language class.

Description:

    This class:
        1) Processes language for agents

"""
# Standard libraries
import os

# Pattoo libraries
from pattoo import log
from pattoo import files


class DataLabelXlate(object):
    """Manage agent languages."""

    def __init__(self, agent_program, _language):
        """Initialize the class.

        Args:
            agent_program: Name of program
            _language: Language of the installation

        Returns:
            None

        """
        # Initialize key variables
        self._agent_program = agent_program
        self._agent_yaml = {}

        # Determine the agent's language yaml file
        root_directory = files.root_directory()
        filepath = (
            '{0}{3}metadata{3}language{3}agents{3}{1}{3}{2}.yaml'.format(
                root_directory, _language, self._agent_program, os.sep))

        # Read the agent's language yaml file
        self._agent_yaml = files.read_yaml_file(filepath, die=False)
        if bool(self._agent_yaml) is False:
            log_message = ('''\
Agent language file {} does not exist for language type "{}" and agent {}. \
You may need to create one or request it as an "issue" on the pattoo GitHub \
site.'''.format(filepath, _language, self._agent_program))
            log.log2warning(1034, log_message)

    def description(self, agent_label):
        """Return the name of the agent.

        Args:
            agent_label: Agent label

        Returns:
            value: Label description

        """
        # Initialize key variables
        value = None
        data = {}
        top_key = 'agent_source_descriptions'

        if top_key in self._agent_yaml:
            data = self._agent_yaml[top_key]

        if agent_label in data:
            if 'description' in data[agent_label]:
                value = data[agent_label]['description']

        # Return
        return value

    def units(self, agent_label):
        """Return the name of the agent.

        Args:
            agent_label: Agent label

        Returns:
            value: Label units of measure

        """
        # Initialize key variables
        value = None
        data = {}
        top_key = 'agent_source_descriptions'

        if top_key in self._agent_yaml:
            data = self._agent_yaml[top_key]

        if agent_label in data:
            if 'units' in data[agent_label]:
                value = data[agent_label]['units']

        # Return
        return value
