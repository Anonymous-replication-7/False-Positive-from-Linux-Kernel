examples = {
    'syz': [
        {'title': '[syzbot] [fs?] INFO: task hung in __generic_file_fsync (5)', 'description': """Hello,

syzbot found the following issue on:

HEAD commit:    32fa4366cc4d net: phy: fix phy_read_poll_timeout argument ..
git tree:       net
console+strace: https://syzkaller.appspot.com/x/log.txt?x=16f5d769180000
kernel config:  https://syzkaller.appspot.com/x/.config?x=6fb1be60a193d440
dashboard link: https://syzkaller.appspot.com/bug?extid=9d95beb2a3c260622518
compiler:       Debian clang version 15.0.6, GNU ld (GNU Binutils for Debian) 2.40
syz repro:      https://syzkaller.appspot.com/x/repro.syz?x=14572985180000
C reproducer:   https://syzkaller.appspot.com/x/repro.c?x=1676fc6e180000

Downloadable assets:
disk image: https://storage.googleapis.com/syzbot-assets/bb05871df8fc/disk-32fa4366.raw.xz
vmlinux: https://storage.googleapis.com/syzbot-assets/a774323fb6ec/vmlinux-32fa4366.xz
kernel image: https://storage.googleapis.com/syzbot-assets/1742ae20d76c/bzImage-32fa4366.xz

IMPORTANT: if you fix the issue, please add the following tag to the commit:
Reported-by: syzbot+9d95beb2a3c260622518@syzkaller.appspotmail.com

============================================
WARNING: possible recursive locking detected
6.8.0-syzkaller-05242-g32fa4366cc4d #0 Not tainted
--------------------------------------------
syz-executor217/5072 is trying to acquire lock:
ffff88802a0fd9f8 (&trie->lock){....}-{2:2}, at: trie_delete_elem+0x96/0x6a0 kernel/bpf/lpm_trie.c:451

but task is already holding lock:
ffff88802a0fc9f8 (&trie->lock){....}-{2:2}, at: trie_update_elem+0xcb/0xc10 kernel/bpf/lpm_trie.c:324

other info that might help us debug this:
 Possible unsafe locking scenario:

       CPU0
       ----
  lock(&trie->lock);
  lock(&trie->lock);

 *** DEADLOCK ***

 May be due to missing lock nesting notation

3 locks held by syz-executor217/5072:
 #0: ffffffff8e131920 (rcu_read_lock){....}-{1:2}, at: rcu_lock_acquire include/linux/rcupdate.h:298 [inline]
 #0: ffffffff8e131920 (rcu_read_lock){....}-{1:2}, at: rcu_read_lock include/linux/rcupdate.h:750 [inline]
 #0: ffffffff8e131920 (rcu_read_lock){....}-{1:2}, at: bpf_map_update_value+0x3c4/0x540 kernel/bpf/syscall.c:202
 #1: ffff88802a0fc9f8 (&trie->lock){....}-{2:2}, at: trie_update_elem+0xcb/0xc10 kernel/bpf/lpm_trie.c:324
 #2: ffffffff8e131920 (rcu_read_lock){....}-{1:2}, at: rcu_lock_acquire include/linux/rcupdate.h:298 [inline]
 #2: ffffffff8e131920 (rcu_read_lock){....}-{1:2}, at: rcu_read_lock include/linux/rcupdate.h:750 [inline]
 #2: ffffffff8e131920 (rcu_read_lock){....}-{1:2}, at: __bpf_trace_run kernel/trace/bpf_trace.c:2380 [inline]
 #2: ffffffff8e131920 (rcu_read_lock){....}-{1:2}, at: bpf_trace_run4+0x16e/0x490 kernel/trace/bpf_trace.c:2422

stack backtrace:
CPU: 0 PID: 5072 Comm: syz-executor217 Not tainted 6.8.0-syzkaller-05242-g32fa4366cc4d #0
Hardware name: Google Google Compute Engine/Google Compute Engine, BIOS Google 02/29/2024
Call Trace:
 <TASK>
 __dump_stack lib/dump_stack.c:88 [inline]
 dump_stack_lvl+0x1e7/0x2e0 lib/dump_stack.c:106
 check_deadlock kernel/locking/lockdep.c:3062 [inline]
 validate_chain+0x15c1/0x58e0 kernel/locking/lockdep.c:3856
 __lock_acquire+0x1346/0x1fd0 kernel/locking/lockdep.c:5137
 lock_acquire+0x1e4/0x530 kernel/locking/lockdep.c:5754
 __raw_spin_lock_irqsave include/linux/spinlock_api_smp.h:110 [inline]
 _raw_spin_lock_irqsave+0xd5/0x120 kernel/locking/spinlock.c:162
 trie_delete_elem+0x96/0x6a0 kernel/bpf/lpm_trie.c:451
 bpf_prog_2c29ac5cdc6b1842+0x42/0x46
 bpf_dispatcher_nop_func include/linux/bpf.h:1234 [inline]
 __bpf_prog_run include/linux/filter.h:657 [inline]
 bpf_prog_run include/linux/filter.h:664 [inline]
 __bpf_trace_run kernel/trace/bpf_trace.c:2381 [inline]
 bpf_trace_run4+0x25a/0x490 kernel/trace/bpf_trace.c:2422
 trace_mm_page_alloc include/trace/events/kmem.h:177 [inline]
 __alloc_pages+0x657/0x680 mm/page_alloc.c:4591
 __alloc_pages_node include/linux/gfp.h:238 [inline]
 alloc_pages_node include/linux/gfp.h:261 [inline]
 __kmalloc_large_node+0x91/0x1f0 mm/slub.c:3926
 __do_kmalloc_node mm/slub.c:3969 [inline]
 __kmalloc_node+0x33c/0x4e0 mm/slub.c:3988
 kmalloc_node include/linux/slab.h:610 [inline]
 bpf_map_kmalloc_node+0xd3/0x1c0 kernel/bpf/syscall.c:422
 lpm_trie_node_alloc kernel/bpf/lpm_trie.c:291 [inline]
 trie_update_elem+0x1d3/0xc10 kernel/bpf/lpm_trie.c:333
 bpf_map_update_value+0x4d3/0x540 kernel/bpf/syscall.c:203
 map_update_elem+0x53a/0x6f0 kernel/bpf/syscall.c:1641
 __sys_bpf+0x76f/0x810 kernel/bpf/syscall.c:5619
 __do_sys_bpf kernel/bpf/syscall.c:5738 [inline]
 __se_sys_bpf kernel/bpf/syscall.c:5736 [inline]
 __x64_sys_bpf+0x7c/0x90 kernel/bpf/syscall.c:5736
 do_syscall_64+0xfb/0x240
 entry_SYSCALL_64_after_hwframe+0x6d/0x75
RIP: 0033:0x7f933485e7a9
Code: 48 83 c4 28 c3 e8 37 17 00 00 0f 1f 80 00 00 00 00 48 89 f8 48 89 f7 48 89 d6 48 89 ca 4d 89 c2 4d 89 c8 4c 8b 4c 24 08 0f 05 <48> 3d 01 f0 ff ff 73 01 c3 48 c7 c1 b8 ff ff ff f7 d8 64 89 01 48
RSP: 002b:00007ffc8852b528 EFLAGS: 00000246 ORIG_RAX: 0000000000000141
RAX: ffffffffffffffda RBX: """},
        
        {'title': 'INFO: task hung in __generic_file_fsync (5)', 'description': """Hello,

syzbot found the following issue on:

HEAD commit:    8155b4ef3466 Add linux-next specific files for 20241220
git tree:       linux-next
console+strace: https://syzkaller.appspot.com/x/log.txt?x=162b26df980000
kernel config:  https://syzkaller.appspot.com/x/.config?x=9c90bb7161a56c88
dashboard link: https://syzkaller.appspot.com/bug?extid=d11add3a08fc150ce457
compiler:       Debian clang version 15.0.6, GNU ld (GNU Binutils for Debian) 2.40
syz repro:      https://syzkaller.appspot.com/x/repro.syz?x=169faaf8580000
C reproducer:   https://syzkaller.appspot.com/x/repro.c?x=12696818580000

Downloadable assets:
disk image: https://storage.googleapis.com/syzbot-assets/98a974fc662d/disk-8155b4ef.raw.xz
vmlinux: https://storage.googleapis.com/syzbot-assets/2dea9b72f624/vmlinux-8155b4ef.xz
kernel image: https://storage.googleapis.com/syzbot-assets/593a42b9eb34/bzImage-8155b4ef.xz
mounted in repro: https://storage.googleapis.com/syzbot-assets/4da9f7f100dd/mount_0.gz

Bisection is inconclusive: the issue happens on the oldest tested release.

bisection log:  https://syzkaller.appspot.com/x/bisect.txt?x=14bdaac4580000
final oops:     https://syzkaller.appspot.com/x/report.txt?x=16bdaac4580000
console output: https://syzkaller.appspot.com/x/log.txt?x=12bdaac4580000

IMPORTANT: if you fix the issue, please add the following tag to the commit:
Reported-by: syzbot+d11add3a08fc150ce457@syzkaller.appspotmail.com

INFO: task syz-executor324:5878 blocked for more than 143 seconds.
      Not tainted 6.13.0-rc3-next-20241220-syzkaller #0
"echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
task:syz-executor324 state:D stack:28912 pid:5878  tgid:5861  ppid:5857   flags:0x00004006
Call Trace:
 <TASK>
 context_switch kernel/sched/core.c:5371 [inline]
 __schedule+0x189f/0x4c80 kernel/sched/core.c:6758
 __schedule_loop kernel/sched/core.c:6835 [inline]
 schedule+0x14b/0x320 kernel/sched/core.c:6850
 schedule_preempt_disabled+0x13/0x30 kernel/sched/core.c:6907
 rwsem_down_write_slowpath+0xeee/0x13b0 kernel/locking/rwsem.c:1176
 __down_write_common kernel/locking/rwsem.c:1304 [inline]
 __down_write kernel/locking/rwsem.c:1313 [inline]
 down_write+0x1d7/0x220 kernel/locking/rwsem.c:1578
 inode_lock include/linux/fs.h:863 [inline]
 __generic_file_fsync+0x97/0x1a0 fs/libfs.c:1537
 generic_file_fsync+0x70/0xf0 fs/libfs.c:1574
 vfs_fsync_range fs/sync.c:187 [inline]
 vfs_fsync fs/sync.c:201 [inline]
 do_fsync fs/sync.c:212 [inline]
 __do_sys_fdatasync fs/sync.c:222 [inline]
 __se_sys_fdatasync fs/sync.c:220 [inline]
 __x64_sys_fdatasync+0xb6/0x110 fs/sync.c:220
 do_syscall_x64 arch/x86/entry/common.c:52 [inline]
 do_syscall_64+0xf3/0x230 arch/x86/entry/common.c:83
 entry_SYSCALL_64_after_hwframe+0x77/0x7f
RIP: 0033:0x7f66848ece09
RSP: 002b:00007f6684882218 EFLAGS: 00000246 ORIG_RAX: 000000000000004b
RAX: ffffffffffffffda RBX: 00007f668497e6d8 RCX: 00007f66848ece09
RDX: 00007f66848ece09 RSI: 0000000000000000 RDI: 0000000000000004
RBP: 00007f668497e6d0 R08: 0000000000000000 R09: 0000000000000000
R10: 00007ffebef38b97 R11: 0000000000000246 R12: 00007f6684941160
R13: 0030656c69662f30 R14: 2f30656c69662f2e R15: 0031656c69662f2e
 </TASK>
INFO: task syz-executor324:5879 blocked for more than 144 seconds.
      Not tainted 6.13.0-rc3-next-20241220-syzkaller #0
"echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
task:syz-executor324 state:D stack:29200 pid:5879  tgid:5862  ppid:5856   flags:0x00004006
Call Trace:
 <TASK>
 context_switch kernel/sched/core.c:5371 [inline]
 __schedule+0x189f/0x4c80 kernel/sched/core.c:6758
 __schedule_loop kernel/sched/core.c:6835 [inline]
 schedule+0x14b/0x320 kernel/sched/core.c:6850
 schedule_preempt_disabled+0x13/0x30 kernel/sched/core.c:6907
 rwsem_down_write_slowpath+0xeee/0x13b0 kernel/locking/rwsem.c:1176
 __down_write_common kernel/locking/rwsem.c:1304 [inline]
 __down_write kernel/locking/rwsem.c:1313 [inline]
 down_write+0x1d7/0x220 kernel/locking/rwsem.c:1578
 inode_lock include/linux/fs.h:863 [inline]
 __generic_file_fsync+0x97/0x1a0 fs/libfs.c:1537
 generic_file_fsync+0x70/0xf0 fs/libfs.c:1574
 vfs_fsync_range fs/sync.c:187 [inline]
 vfs_fsync fs/sync.c:201 [inline]
 do_fsync fs/sync.c:212 [inline]
 __do_sys_fdatasync fs/sync.c:222 [inline]
 __se_sys_fdatasync fs/sync.c:220 [inline]
 __x64_sys_fdatasync+0xb6/0x110 fs/sync.c:220
 do_syscall_x64 arch/x86/entry/common.c:52 [inline]
 do_syscall_64+0xf3/0x230 arch/x86/entry/common.c:83
 entry_SYSCALL_64_after_hwframe+0x77/0x7f
RIP: 0033:0x7f66848ece09
RSP: 002b:00007f6684882218 EFLAGS: 00000246 ORIG_RAX: 000000000000004b
RAX: ffffffffffffffda RBX: 00007f668497e6d8 RCX: 00007f66848ece09
RDX: 00007f66848c63c6 RSI: 0000000000000000 RDI: 0000000000000004
RBP: 00007f668497e6d0 R08: 00007ffebef38b97 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 00007f6684941160
R13: 0030656c69662f30 R14: 2f30656c69662f2e R15: 0031656c69662f2e
 </TASK>
INFO: task syz-executor324:5874 blocked for more than 145 seconds.
      Not tainted 6.13.0-rc3-next-20241220-syzkaller #0
"echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
task:syz-executor324 state:D stack:28632 pid:5874  tgid:5863  ppid:5858   flags:0x00004006
Call Trace:
 <TASK>
 context_switch kernel/sched/core.c:5371 [inline]
 __schedule+0x189f/0x4c80 kernel/sched/core.c:6758
 __schedule_loop kernel/sched/core.c:6835 [inline]
 schedule+0x14b/0x320 kernel/sched/core.c:6850
 schedule_preempt_disabled+0x13/0x30 kernel/sched/core.c:6907
 rwsem_down_write_slowpath+0xeee/0x13b0 kernel/locking/rwsem.c:1176
 __down_write_common kernel/locking/rwsem.c:1304 [inline]
 __down_write kernel/locking/rwsem.c:1313 [inline]
 down_write+0x1d7/0x220 kernel/locking/rwsem.c:1578
 inode_lock include/linux/fs.h:863 [inline]
 __generic_file_fsync+0x97/0x1a0 fs/libfs.c:1537
 generic_file_fsync+0x70/0xf0 fs/libfs.c:1574
 vfs_fsync_range fs/sync.c:187 [inline]
 vfs_fsync fs/sync.c:201 [inline]
 do_fsync fs/sync.c:212 [inline]
 __do_sys_fdatasync fs/sync.c:222 [inline]
 __se_sys_fdatasync fs/sync.c:220 [inline]
 __x64_sys_fdatasync+0xb6/0x110 fs/sync.c:220
 do_syscall_x64 arch/x86/entry/common.c:52 [inline]
 do_syscall_64+0xf3/0x230 arch/x86/entry/common.c:83
 entry_SYSCALL_64_after_hwframe+0x77/0x7f
RIP: 0033:0x7f66848ece09
RSP: 002b:00007f6684882218 EFLAGS: 00000246 ORIG_RAX: 000000000000004b
RAX: ffffffffffffffda RBX: 00007f668497e6d8 RCX: 00007f66848ece09
RDX: 00007f66848c63c6 RSI: 0000000000000000 RDI: 0000000000000004
RBP: 00007f668497e6d0 R08: 00007ffebef38b97 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 00007f6684941160
R13: 0030656c69662f30 R14: 2f30656c69662f2e R15: 0031656c69662f2e
 </TASK>
INFO: task syz-executor324:5876 blocked for more than 145 seconds.
      Not tainted 6.13.0-rc3-next-20241220-syzkaller #0
"echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
task:syz-executor324 state:D stack:29200 pid:5876  tgid:5866  ppid:5859   flags:0x00004006
Call Trace:
 <TASK>
 context_switch kernel/sched/core.c:5371 [inline]
 __schedule+0x189f/0x4c80 kernel/sched/core.c:6758
 __schedule_loop kernel/sched/core.c:6835 [inline]
 schedule+0x14b/0x320 kernel/sched/core.c:6850
 schedule_preempt_disabled+0x13/0x30 kernel/sched/core.c:6907
 rwsem_down_write_slowpath+0xeee/0x13b0 kernel/locking/rwsem.c:1176
 __down_write_common kernel/locking/rwsem.c:1304 [inline]
 __down_write kernel/locking/rwsem.c:1313 [inline]
 down_write+0x1d7/0x220 kernel/locking/rwsem.c:1578
 inode_lock include/linux/fs.h:863 [inline]
 __generic_file_fsync+0x97/0x1a0 fs/libfs.c:1537
 generic_file_fsync+0x70/0xf0 fs/libfs.c:1574
 vfs_fsync_range fs/sync.c:187 [inline]
 vfs_fsync fs/sync.c:201 [inline]
 do_fsync fs/sync.c:212 [inline]
 __do_sys_fdatasync fs/sync.c:222 [inline]
 __se_sys_fdatasync fs/sync.c:220 [inline]
 __x64_sys_fdatasync+0xb6/0x110 fs/sync.c:220
 do_syscall_x64 arch/x86/entry/common.c:52 [inline]
 do_syscall_64+0xf3/0x230 arch/x86/entry/common.c:83
 entry_SYSCALL_64_after_hwframe+0x77/0x7f
RIP: 0033:0x7f66848ece09
RSP: 002b:00007f6684882218 EFLAGS: 00000246 ORIG_RAX: 000000000000004b
RAX: ffffffffffffffda RBX: 00007f668497e6d8 RCX: 00007f66848ece09
RDX: 00007f66848c63c6 RSI: 0000000000000000 RDI: 0000000000000004
RBP: 00007f668497e6d0 R08: 00007ffebef38b97 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 00007f6684941160
R13: 0030656c69662f30 R14: 2f30656c69662f2e R15: 0031656c69662f2e
 </TASK>
INFO: task syz-executor324:5877 blocked for more than 146 seconds.
      Not tainted 6.13.0-rc3-next-20241220-syzkaller #0
"echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
task:syz-executor324 state:D stack:28912 pid:5877  tgid:5865  ppid:5860   flags:0x00004006
Call Trace:
 <TASK>
 context_switch kernel/sched/core.c:5371 [inline]
 __schedule+0x189f/0x4c80 kernel/sched/core.c:6758
 __schedule_loop kernel/sched/core.c:6835 [inline]
 schedule+0x14b/0x320 kernel/sched/core.c:6850
 schedule_preempt_disabled+0x13/0x30 kernel/sched/core.c:6907
 rwsem_down_write_slowpath+0xeee/0x13b0 kernel/locking/rwsem.c:1176
 __down_write_common kernel/locking/rwsem.c:1304 [inline]
 __down_write kernel/locking/rwsem.c:1313 [inline]
 down_write+0x1d7/0x220 kernel/locking/rwsem.c:1578
 inode_lock include/linux/fs.h:863 [inline]
 __generic_file_fsync+0x97/0x1a0 fs/libfs.c:1537
 generic_file_fsync+0x70/0xf0 fs/libfs.c:1574
 vfs_fsync_range fs/sync.c:187 [inline]
 vfs_fsync fs/sync.c:201 [inline]
 do_fsync fs/sync.c:212 [inline]
 __do_sys_fdatasync fs/sync.c:222 [inline]
 __se_sys_fdatasync fs/sync.c:220 [inline]
 __x64_sys_fdatasync+0xb6/0x110 fs/sync.c:220
 do_syscall_x64 arch/x86/entry/common.c:52 [inline]
 do_syscall_64+0xf3/0x230 arch/x86/entry/common.c:83
 entry_SYSCALL_64_after_hwframe+0x77/0x7f
RIP: 0033:0x7f66848ece09
RSP: 002b:00007f6684882218 EFLAGS: 00000246 ORIG_RAX: 000000000000004b
RAX: ffffffffffffffda RBX: 00007f668497e6d8 RCX: 00007f66848ece09
RDX: 00007f66848ece09 RSI: 0000000000000000 RDI: 0000000000000004
RBP: 00007f668497e6d0 R08: 0000000000000000 R09: 0000000000000000
R10: 00007ffebef38b97 R11: 0000000000000246 R12: 00007f6684941160
R13: 0030656c69662f30 R14: 2f30656c69662f2e R15: 0031656c69662f2e
 </TASK>

Showing all locks held in the system:
1 lock held by khungtaskd/30:
 #0: ffffffff8e937da0 (rcu_read_lock){....}-{1:3}, at: rcu_lock_acquire include/linux/rcupdate.h:337 [inline]
 #0: ffffffff8e937da0 (rcu_read_lock){....}-{1:3}, at: rcu_read_lock include/linux/rcupdate.h:849 [inline]
 #0: ffffffff8e937da0 (rcu_read_lock){....}-{1:3}, at: debug_show_all_locks+0x55/0x2a0 kernel/locking/lockdep.c:6744
1 lock held by kswapd0/89:
1 lock held by kswapd1/90:
2 locks held by getty/5589:
 #0: ffff88814d95d0a0 (&tty->ldisc_sem){++++}-{0:0}, at: tty_ldisc_ref_wait+0x25/0x70 drivers/tty/tty_ldisc.c:243
 #1: ffffc90002fde2f0 (&ldata->atomic_read_lock){+.+.}-{4:4}, at: n_tty_read+0x6a6/0x1e00 drivers/tty/n_tty.c:2211
1 lock held by syz-executor324/5869:
1 lock held by syz-executor324/5878:
 #0: ffff88807ba6c180 (&type->i_mutex_dir_key#6){++++}-{4:4}, at: inode_lock include/linux/fs.h:863 [inline]
 #0: ffff88807ba6c180 (&type->i_mutex_dir_key#6){++++}-{4:4}, at: __generic_file_fsync+0x97/0x1a0 fs/libfs.c:1537
1 lock held by syz-executor324/5872:
1 lock held by syz-executor324/5879:
 #0: ffff88807ba6cc00 (&type->i_mutex_dir_key#6){++++}-{4:4}, at: inode_lock include/linux/fs.h:863 [inline]
 #0: ffff88807ba6cc00 (&type->i_mutex_dir_key#6){++++}-{4:4}, at: __generic_file_fsync+0x97/0x1a0 fs/libfs.c:1537
1 lock held by syz-executor324/5870:
1 lock held by syz-executor324/5874:
 #0: ffff88807ba64180 (&type->i_mutex_dir_key#6){++++}-{4:4}, at: inode_lock include/linux/fs.h:863 [inline]
 #0: ffff88807ba64180 (&type->i_mutex_dir_key#6){++++}-{4:4}, at: __generic_file_fsync+0x97/0x1a0 fs/libfs.c:1537
2 locks held by syz-executor324/5871:
1 lock held by syz-executor324/5876:
 #0: ffff88807ba646c0 (&type->i_mutex_dir_key#6){++++}-{4:4}, at: inode_lock include/linux/fs.h:863 [inline]
 #0: ffff88807ba646c0 (&type->i_mutex_dir_key#6){++++}-{4:4}, at: __generic_file_fsync+0x97/0x1a0 fs/libfs.c:1537
5 locks held by syz-executor324/5873:
1 lock held by syz-executor324/5877:
 #0: ffff88807ba6c6c0 (&type->i_mutex_dir_key#6){++++}-{4:4}, at: inode_lock include/linux/fs.h:863 [inline]
 #0: ffff88807ba6c6c0 (&type->i_mutex_dir_key#6){++++}-{4:4}, at: __generic_file_fsync+0x97/0x1a0 fs/libfs.c:1537

=============================================

NMI backtrace for cpu 1
CPU: 1 UID: 0 PID: 30 Comm: khungtaskd Not tainted 6.13.0-rc3-next-20241220-syzkaller #0
Hardware name: Google Google Compute Engine/Google Compute Engine, BIOS Google 09/13/2024
Call Trace:
 <TASK>
 __dump_stack lib/dump_stack.c:94 [inline]
 dump_stack_lvl+0x241/0x360 lib/dump_stack.c:120
 nmi_cpu_backtrace+0x49c/0x4d0 lib/nmi_backtrace.c:113
 nmi_trigger_cpumask_backtrace+0x198/0x320 lib/nmi_backtrace.c:62
 trigger_all_cpu_backtrace include/linux/nmi.h:162 [inline]
 check_hung_uninterruptible_tasks kernel/hung_task.c:234 [inline]
 watchdog+0xff6/0x1040 kernel/hung_task.c:397
 kthread+0x7a9/0x920 kernel/kthread.c:464
 ret_from_fork+0x4b/0x80 arch/x86/kernel/process.c:148
 ret_from_fork_asm+0x1a/0x30 arch/x86/entry/entry_64.S:244
 </TASK>
Sending NMI from CPU 1 to CPUs 0:
NMI backtrace for cpu 0
CPU: 0 UID: 0 PID: 5871 Comm: syz-executor324 Not tainted 6.13.0-rc3-next-20241220-syzkaller #0
Hardware name: Google Google Compute Engine/Google Compute Engine, BIOS Google 09/13/2024
RIP: 0010:check_kcov_mode kernel/kcov.c:185 [inline]
RIP: 0010:write_comp_data kernel/kcov.c:246 [inline]
RIP: 0010:__sanitizer_cov_trace_const_cmp4+0x2f/0x90 kernel/kcov.c:314
Code: 8b 04 24 65 48 8b 14 25 c0 d6 03 00 65 8b 05 50 ae 44 7e 25 00 01 ff 00 74 10 3d 00 01 00 00 75 5b 83 ba 24 16 00 00 00 74 52 <8b> 82 00 16 00 00 83 f8 03 75 47 48 8b 8a 08 16 00 00 44 8b 8a 04
RSP: 0018:ffffc900041ced78 EFLAGS: 00000246
RAX: 0000000000000000 RBX: 0000000000000001 RCX: ffff888078ef9e00
RDX: ffff888078ef9e00 RSI: 0000000000000001 RDI: 0000000000000000
RBP: ffffc900041cee80 R08: ffffffff81f7ce68 R09: 1ffffffff285af08
R10: dffffc0000000000 R11: fffffbfff285af09 R12: 0000000000000000
R13: dffffc0000000000 R14: ffffc900041cedd8 R15: ffffc900041cedc0
FS:  00007f66848a36c0(0000) GS:ffff8880b8600000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 00007efd57688580 CR3: 000000002506c000 CR4: 00000000003526f0
DR0: 0000000000000000 DR1: 0000000000000000 DR2: 0000000000000000
DR3: 0000000000000000 DR6: 00000000fffe0ff0 DR7: 0000000000000400
Call Trace:
 <NMI>
 </NMI>
 <TASK>
 rcu_read_lock include/linux/rcupdate.h:850 [inline]
 filemap_get_entry+0x158/0x3b0 mm/filemap.c:1820
 __filemap_get_folio+0x72/0x940 mm/filemap.c:1868
 __find_get_block_slow fs/buffer.c:203 [inline]
 __find_get_block+0x287/0x1140 fs/buffer.c:1398
 bdev_getblk+0x33/0x670 fs/buffer.c:1425
 __bread_gfp+0x86/0x400 fs/buffer.c:1485
 sb_bread include/linux/buffer_head.h:346 [inline]
 get_branch+0x2c3/0x6e0 fs/sysv/itree.c:102
 get_block+0x180/0x16d0 fs/sysv/itree.c:222
 block_read_full_folio+0x3ee/0xae0 fs/buffer.c:2396
 filemap_read_folio+0x148/0x3b0 mm/filemap.c:2348
 do_read_cache_folio+0x373/0x5b0 mm/filemap.c:3893
 read_mapping_folio include/linux/pagemap.h:1032 [inline]
 dir_get_folio fs/sysv/dir.c:64 [inline]
 sysv_find_entry+0x16c/0x590 fs/sysv/dir.c:154
 sysv_inode_by_name+0x98/0x2a0 fs/sysv/dir.c:370
 sysv_lookup+0x6b/0xe0 fs/sysv/namei.c:38
 __lookup_slow+0x28c/0x3f0 fs/namei.c:1791
 lookup_slow+0x53/0x70 fs/namei.c:1808
 walk_component fs/namei.c:2112 [inline]
 link_path_walk+0x99b/0xea0 fs/namei.c:2477
 path_parentat fs/namei.c:2681 [inline]
 __filename_parentat+0x2a7/0x740 fs/namei.c:2705
 filename_parentat fs/namei.c:2723 [inline]
 do_renameat2+0x3b8/0x13f0 fs/namei.c:5136
 __do_sys_rename fs/namei.c:5271 [inline]
 __se_sys_rename fs/namei.c:5269 [inline]
 __x64_sys_rename+0x82/0x90 fs/namei.c:5269
 do_syscall_x64 arch/x86/entry/common.c:52 [inline]
 do_syscall_64+0xf3/0x230 arch/x86/entry/common.c:83
 entry_SYSCALL_64_after_hwframe+0x77/0x7f
RIP: 0033:0x7f66848ece09
Code: 28 00 00 00 75 05 48 83 c4 28 c3 e8 b1 18 00 00 90 48 89 f8 48 89 f7 48 89 d6 48 89 ca 4d 89 c2 4d 89 c8 4c 8b 4c 24 08 0f 05 <48> 3d 01 f0 ff ff 73 01 c3 48 c7 c1 b0 ff ff ff f7 d8 64 89 01 48
RSP: 002b:00007f66848a3218 EFLAGS: 00000246 ORIG_RAX: 0000000000000052
RAX: ffffffffffffffda RBX: 00007f668497e6c8 RCX: 00007f66848ece09
RDX: ffffffffffffffb0 RSI: 0000000020000000 RDI: 0000000020000040
RBP: 00007f668497e6c0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 00007f6684941160
R13: 0030656c69662f30 R14: 2f30656c69662f2e R15: 0031656c69662f2e
 </TASK>"""}    
    ],
    'bugzilla': [
        {'title': 'stack-buffer-overflow on i2ctransfer with large arg', 'description': """I clone git://git.kernel.org/pub/scm/utils/i2c-tools/i2c-tools.git and build it with asan/ubsan.


```
# i2ctransfer -V
i2ctransfer version 4.4+git
```

And I run i2ctransfer with large arg.

```
# i2ctransfer -fy 2 w1@0x77 0x00 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3 r3  r3 r3 r3 r3 r3
tools/i2ctransfer.c:257:8: runtime error: index 42 out of bounds for type 'i2c_msg [42]'
tools/i2ctransfer.c:257:21: runtime error: store to address 0x7e973ab8 with insufficient space for an object of type '__u16'
0x7e973ab8: note: pointer points here
 90 02 c0 74  08 ac fc 76 fc 3a 97 7e  f8 3a 97 7e 30 2a 00 75  00 00 00 00 00 b0 85 18  f8 80 fc 76
              ^ 
=================================================================
==4267==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7e973ab8 at pc 0x000f00a0 bp 0x7e973798 sp 0x7e973798
WRITE of size 2 at 0x7e973ab8 thread T0
    #0 0xf009c in main (/tmp/yuan_i2ctransfer+0xf009c)
    #1 0x76d85d48 in __libc_start_main (/lib/libc.so.6+0x1ad48)

Address 0x7e973ab8 is located in stack of thread T0 at offset 664 in frame
    #0 0xeecec in main (/tmp/yuan_i2ctransfer+0xeecec)

  This frame has 4 object(s):
    [48, 52) 'end' (line 194)
    [64, 72) 'rdwr' (line 334)
    [96, 116) 'filename' (line 145)
    [160, 664) 'msgs' (line 148) <== Memory access at offset 664 overflows this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
Shadow bytes around the buggy address:
  0x2fd2e700: 00 00 00 00 f1 f1 f1 f1 f1 f1 04 f2 00 f2 f2 f2
  0x2fd2e710: 00 00 04 f2 f2 f2 f2 f2 00 00 00 00 00 00 00 00
  0x2fd2e720: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x2fd2e730: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x2fd2e740: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x2fd2e750: 00 00 00 00 00 00 00[f3]f3 f3 f3 f3 f3 f3 f3 f3
  0x2fd2e760: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x2fd2e770: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x2fd2e780: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x2fd2e790: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x2fd2e7a0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==4267==ABORTING
```"""},
        {'title': 'Broadcast RGB is set to Limited but should be Full RGB', 'description': 
            """Created attachment 286445 [details]
xrandr log
I have P2419H Dell monitor connected to my laptop via DisplayPort cable (no adapters, my HP laptop has DP port). Graphics card is Intel HD 4000 (Ivy Bridge) integrated into CPU Intel i5 3360m. No other dedicate graphics card is present. Tough Full RGB should be set for this monitor, Limited RGB is always set on boot. It looks similar to this problem: https://bugzilla.kernel.org/show_bug.cgi?id=94921
Verbose information from xrandr included in attachment."""}    
    ]
}