from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from typing import Any

from . import (
    callback,
    frame,
    spec,
)
from . import (
    connection as connection_,
)

MAX_CHANNELS: int

type _OnAckNackCallback = Callable[[frame.Method[spec.Basic.Ack | spec.Basic.Nack]], None]
type _OnConfirmDeliveryCallback = Callable[[frame.Method[spec.Confirm.SelectOk]], None]
type _OnBasicConsumeCallback = Callable[[frame.Method[spec.Basic.ConsumeOk]], None]
type _OnBasicGetCallback = Callable[
    [Channel, spec.Basic.GetOk, spec.BasicProperties, bytes], None
]
type _OnBasicRecoverCallback = Callable[[frame.Method[spec.Basic.RecoverOk]], None]
type _OnBasicQosCallback = Callable[[frame.Method[spec.Basic.QosOk]], None]
type _OnBasicCancelCallback = Callable[[frame.Method[spec.Basic.CancelOk]], None]
type _OnCloseCallback = Callable[[Channel, Exception], None]

type _OnExchangeBindCallback = Callable[[frame.Method[spec.Exchange.BindOk]], None]
type _OnExchangeDeclareCallback = Callable[[frame.Method[spec.Exchange.DeclareOk]], None]
type _OnExchangeDeleteCallback = Callable[[frame.Method[spec.Exchange.DeleteOk]], None]
type _OnExchangeUnbindCallback = Callable[[frame.Method[spec.Exchange.UnbindOk]], None]
type _OnFlowCallback = Callable[[bool], None]
type _OnMessageCallback = Callable[
    [Channel, spec.Basic.Deliver, spec.BasicProperties, bytes], None
]
type _OnOpenCallback = Callable[[Channel], None]
type _OnQueueBindCallback = Callable[[frame.Method[spec.Queue.BindOk]], None]
type _OnQueueDeclareCallback = Callable[[frame.Method[spec.Queue.DeclareOk]], None]
type _OnQueueDeleteCallback = Callable[[frame.Method[spec.Queue.DeleteOk]], None]
type _OnQueuePurgeCallback = Callable[[frame.Method[spec.Queue.PurgeOk]], None]
type _OnQueueUnbindCallback = Callable[[frame.Method[spec.Queue.UnbindOk]], None]
type _OnReturnCallback = Callable[
    [Channel, spec.Basic.Return, spec.BasicProperties, bytes], None
]
type _OnTxCommitCallback = Callable[[spec.Tx.CommitOk], None]
type _OnTxRollbackCallback = Callable[[spec.Tx.RollbackOk], None]
type _OnTxSelectCallback = Callable[[spec.Tx.SelectOk], None]

class Channel:
    CLOSED: int = ...
    OPENING: int = ...
    OPEN: int = ...
    CLOSING: int = ...

    channel_number: int = ...
    callbacks: callback.CallbackManager = ...
    connection: connection_.Connection = ...
    flow_active: bool = ...

    def __init__(
        self,
        connection: connection_.Connection,
        channel_number: int,
        on_open_callback: _OnOpenCallback,
    ) -> None: ...
    def __int__(self) -> int: ...
    def add_callback(
        self,
        callback: Callable[..., Any],
        replies: Sequence[Any],
        one_shot: bool = ...,
    ) -> None: ...
    def add_on_cancel_callback(self, callback: _OnBasicCancelCallback) -> None: ...
    def add_on_close_callback(self, callback: _OnCloseCallback) -> None: ...
    def add_on_flow_callback(self, callback: _OnFlowCallback) -> None: ...
    def add_on_return_callback(self, callback: _OnReturnCallback) -> None: ...
    def basic_ack(
        self,
        delivery_tag: int = ...,
        multiple: bool = ...,
    ) -> None: ...
    def basic_cancel(
        self,
        consumer_tag: str = ...,
        callback: _OnBasicCancelCallback | None = ...,
    ) -> None: ...
    def basic_consume(
        self,
        queue: str,
        on_message_callback: _OnMessageCallback,
        auto_ack: bool = ...,
        exclusive: bool = ...,
        consumer_tag: str | None = ...,
        arguments: Mapping[str, Any] | None = ...,
        callback: _OnBasicConsumeCallback | None = ...,
    ) -> str: ...
    def basic_get(
        self,
        queue: str,
        callback: _OnBasicGetCallback,
        auto_ack: bool = ...,
    ) -> None: ...
    def basic_nack(
        self,
        delivery_tag: int | None = ...,
        multiple: bool = ...,
        requeue: bool = ...,
    ) -> None: ...
    def basic_publish(
        self,
        exchange: str,
        routing_key: str,
        body: bytes,
        properties: spec.BasicProperties | None = ...,
        mandatory: bool = ...,
    ) -> None: ...
    def basic_qos(
        self,
        prefetch_size: int = ...,
        prefetch_count: int = ...,
        global_qos: bool = ...,
        callback: _OnBasicQosCallback | None = ...,
    ) -> None: ...
    def basic_reject(self, delivery_tag: int, requeue: bool = ...) -> None: ...
    def basic_recover(
        self,
        requeue: bool = ...,
        callback: _OnBasicRecoverCallback | None = ...,
    ) -> None: ...
    def close(self, reply_code: int = ..., reply_text: str = ...) -> None: ...
    def confirm_delivery(
        self,
        ack_nack_callback: _OnAckNackCallback,
        callback: _OnConfirmDeliveryCallback | None = ...,
    ) -> None: ...
    @property
    def consumer_tags(self) -> list[str]: ...
    def exchange_bind(
        self,
        destination: str,
        source: str,
        routing_key: str = ...,
        arguments: Mapping[str, Any] | None = ...,
        callback: _OnExchangeBindCallback | None = ...,
    ) -> None: ...
    def exchange_declare(
        self,
        exchange: str,
        exchange_type: str = ...,
        passive: bool = ...,
        durable: bool = ...,
        auto_delete: bool = ...,
        internal: bool = ...,
        arguments: Mapping[str, Any] | None = ...,
        callback: _OnExchangeDeclareCallback | None = ...,
    ) -> None: ...
    def exchange_delete(
        self,
        exchange: str | None = ...,
        if_unused: bool = ...,
        callback: _OnExchangeDeleteCallback | None = ...,
    ) -> None: ...
    def exchange_unbind(
        self,
        destination: str | None = ...,
        source: str | None = ...,
        routing_key: str = ...,
        arguments: Mapping[str, Any] | None = ...,
        callback: _OnExchangeUnbindCallback | None = ...,
    ) -> None: ...
    def flow(self, active: bool, callback: _OnFlowCallback | None = ...) -> None: ...
    @property
    def is_closed(self) -> bool: ...
    @property
    def is_closing(self) -> bool: ...
    @property
    def is_open(self) -> bool: ...
    def open(self) -> None: ...
    def queue_bind(
        self,
        queue: str,
        exchange: str,
        routing_key: str | None = ...,
        arguments: Mapping[str, Any] | None = ...,
        callback: _OnQueueBindCallback | None = ...,
    ) -> None: ...
    def queue_declare(
        self,
        queue: str,
        passive: bool = ...,
        durable: bool = ...,
        exclusive: bool = ...,
        auto_delete: bool = ...,
        arguments: Mapping[str, Any] | None = ...,
        callback: _OnQueueDeclareCallback | None = ...,
    ) -> None: ...
    def queue_delete(
        self,
        queue: str,
        if_unused: bool = ...,
        if_empty: bool = ...,
        callback: _OnQueueDeleteCallback | None = ...,
    ) -> None: ...
    def queue_purge(
        self,
        queue: str,
        callback: _OnQueuePurgeCallback | None = ...,
    ) -> None: ...
    def queue_unbind(
        self,
        queue: str,
        exchange: str | None = ...,
        routing_key: str | None = ...,
        arguments: Mapping[str, Any] | None = ...,
        callback: _OnQueueUnbindCallback | None = ...,
    ) -> None: ...
    def tx_commit(self, callback: _OnTxCommitCallback | None = ...) -> None: ...
    def tx_rollback(self, callback: _OnTxRollbackCallback | None = ...) -> None: ...
    def tx_select(self, callback: _OnTxSelectCallback | None = ...) -> None: ...
