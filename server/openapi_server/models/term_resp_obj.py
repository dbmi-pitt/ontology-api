# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class TermRespObj(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, code_id=None, code_sab=None, code=None, concept=None, tty=None, term=None, matched=None, rel_type=None, rel_sab=None):  # noqa: E501
        """TermRespObj - a model defined in OpenAPI

        :param code_id: The code_id of this TermRespObj.  # noqa: E501
        :type code_id: str
        :param code_sab: The code_sab of this TermRespObj.  # noqa: E501
        :type code_sab: str
        :param code: The code of this TermRespObj.  # noqa: E501
        :type code: str
        :param concept: The concept of this TermRespObj.  # noqa: E501
        :type concept: str
        :param tty: The tty of this TermRespObj.  # noqa: E501
        :type tty: str
        :param term: The term of this TermRespObj.  # noqa: E501
        :type term: str
        :param matched: The matched of this TermRespObj.  # noqa: E501
        :type matched: str
        :param rel_type: The rel_type of this TermRespObj.  # noqa: E501
        :type rel_type: str
        :param rel_sab: The rel_sab of this TermRespObj.  # noqa: E501
        :type rel_sab: str
        """
        self.openapi_types = {
            'code_id': str,
            'code_sab': str,
            'code': str,
            'concept': str,
            'tty': str,
            'term': str,
            'matched': str,
            'rel_type': str,
            'rel_sab': str
        }

        self.attribute_map = {
            'code_id': 'code_id',
            'code_sab': 'code_sab',
            'code': 'code',
            'concept': 'concept',
            'tty': 'tty',
            'term': 'term',
            'matched': 'matched',
            'rel_type': 'rel_type',
            'rel_sab': 'rel_sab'
        }

        self._code_id = code_id
        self._code_sab = code_sab
        self._code = code
        self._concept = concept
        self._tty = tty
        self._term = term
        self._matched = matched
        self._rel_type = rel_type
        self._rel_sab = rel_sab

    @classmethod
    def from_dict(cls, dikt) -> 'TermRespObj':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The TermRespObj of this TermRespObj.  # noqa: E501
        :rtype: TermRespObj
        """
        return util.deserialize_model(dikt, cls)

    @property
    def code_id(self):
        """Gets the code_id of this TermRespObj.


        :return: The code_id of this TermRespObj.
        :rtype: str
        """
        return self._code_id

    @code_id.setter
    def code_id(self, code_id):
        """Sets the code_id of this TermRespObj.


        :param code_id: The code_id of this TermRespObj.
        :type code_id: str
        """

        self._code_id = code_id

    @property
    def code_sab(self):
        """Gets the code_sab of this TermRespObj.


        :return: The code_sab of this TermRespObj.
        :rtype: str
        """
        return self._code_sab

    @code_sab.setter
    def code_sab(self, code_sab):
        """Sets the code_sab of this TermRespObj.


        :param code_sab: The code_sab of this TermRespObj.
        :type code_sab: str
        """

        self._code_sab = code_sab

    @property
    def code(self):
        """Gets the code of this TermRespObj.


        :return: The code of this TermRespObj.
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this TermRespObj.


        :param code: The code of this TermRespObj.
        :type code: str
        """

        self._code = code

    @property
    def concept(self):
        """Gets the concept of this TermRespObj.


        :return: The concept of this TermRespObj.
        :rtype: str
        """
        return self._concept

    @concept.setter
    def concept(self, concept):
        """Sets the concept of this TermRespObj.


        :param concept: The concept of this TermRespObj.
        :type concept: str
        """

        self._concept = concept

    @property
    def tty(self):
        """Gets the tty of this TermRespObj.


        :return: The tty of this TermRespObj.
        :rtype: str
        """
        return self._tty

    @tty.setter
    def tty(self, tty):
        """Sets the tty of this TermRespObj.


        :param tty: The tty of this TermRespObj.
        :type tty: str
        """

        self._tty = tty

    @property
    def term(self):
        """Gets the term of this TermRespObj.


        :return: The term of this TermRespObj.
        :rtype: str
        """
        return self._term

    @term.setter
    def term(self, term):
        """Sets the term of this TermRespObj.


        :param term: The term of this TermRespObj.
        :type term: str
        """

        self._term = term

    @property
    def matched(self):
        """Gets the matched of this TermRespObj.


        :return: The matched of this TermRespObj.
        :rtype: str
        """
        return self._matched

    @matched.setter
    def matched(self, matched):
        """Sets the matched of this TermRespObj.


        :param matched: The matched of this TermRespObj.
        :type matched: str
        """

        self._matched = matched

    @property
    def rel_type(self):
        """Gets the rel_type of this TermRespObj.


        :return: The rel_type of this TermRespObj.
        :rtype: str
        """
        return self._rel_type

    @rel_type.setter
    def rel_type(self, rel_type):
        """Sets the rel_type of this TermRespObj.


        :param rel_type: The rel_type of this TermRespObj.
        :type rel_type: str
        """

        self._rel_type = rel_type

    @property
    def rel_sab(self):
        """Gets the rel_sab of this TermRespObj.


        :return: The rel_sab of this TermRespObj.
        :rtype: str
        """
        return self._rel_sab

    @rel_sab.setter
    def rel_sab(self, rel_sab):
        """Sets the rel_sab of this TermRespObj.


        :param rel_sab: The rel_sab of this TermRespObj.
        :type rel_sab: str
        """

        self._rel_sab = rel_sab
